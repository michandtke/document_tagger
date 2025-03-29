import logging
import numpy as np
from sentence_transformers import SentenceTransformer
from services.text_extraction import TextExtractor

class SimilarityService:
    """
    Service for calculating similarities between documents and queries
    """
    
    def __init__(self, document_service, model_name='all-MiniLM-L6-v2'):
        """
        Initialize similarity service
        
        Args:
            document_service: Document service for accessing documents
            model_name (str): Name of the SentenceTransformer model
        """
        self.document_service = document_service
        self.logger = logging.getLogger(__name__)
        self.text_extractor = TextExtractor()
        
        # Initialize embedding model
        self.logger.info(f"Loading embedding model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            self.logger.info("Embedding model loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading embedding model: {str(e)}")
            self.model = None
    
    def calculate_similarities_from_file(self, file_data, filename, tags=None):
        """
        Calculate similarities from file data by first extracting text
        
        Args:
            file_data (bytes): Binary file data
            filename (str): Original filename
            tags (str, optional): Tags to use as fallback if text extraction fails
            
        Returns:
            tuple: (similarity_dict, sorted_documents, tag_suggestions)
        """
        self.logger.info(f"Calculating similarities for file: {filename}")
        
        # Extract text from the file
        extracted_text = self.text_extractor.extract_text(file_data, filename)
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            self.logger.warning(f"Text extraction produced little or no content from {filename}")
            # Fall back to tags if text extraction fails
            if tags:
                self.logger.info(f"Using tags as fallback: {tags}")
                return self.calculate_similarities(tags)
            return {}, [], []
        
        self.logger.info(f"Extracted {len(extracted_text)} characters of text")
        
        # Use the extracted text for similarity calculation
        return self.calculate_similarities(extracted_text)
    
    def calculate_similarities(self, text_content, existing_docs=None):
        """
        Calculate similarities between text content and documents
        
        Args:
            text_content (str): Text to compare with documents
            existing_docs (list, optional): List of documents with embeddings.
                                        If None, will fetch all documents.
        
        Returns:
            tuple: (similarity_dict, sorted_documents, tag_suggestions)
        """
        self.logger.info(f"Calculating similarities for text: {text_content[:50]}...")
        
        # Generate embedding for the content
        content_embedding = self.generate_embedding(text_content)
        
        if not content_embedding:
            self.logger.error("Failed to generate embedding for content")
            return {}, [], []
            
        self.logger.info(f"Generated embedding with length: {len(content_embedding)}")
        
        # Get all documents if not provided
        documents = existing_docs
        if documents is None:
            documents = self.document_service.get_all_documents()
        
        self.logger.info(f"Comparing with {len(documents)} documents")
        
        # Calculate similarity with each document
        similarity_data = {}
        doc_similarities = []
        
        for doc in documents:
            doc_embedding = doc.get('embedding', [])
            
            if doc_embedding and len(doc_embedding) > 0:
                similarity = self.compute_similarity(content_embedding, doc_embedding)
                similarity_value = round(similarity * 100)  # Convert to percentage
                
                # Store in dictionary with ID as key
                similarity_data[doc['id']] = similarity_value
                
                # Also update the similarity in the document for sorting
                doc['similarity'] = similarity_value
                
                # Get tags as string if they're a list
                tags = doc['tags']
                if isinstance(tags, list):
                    tags_str = ", ".join(tags)
                else:
                    tags_str = tags
                
                # Store document info with similarity for tag suggestions
                doc_similarities.append({
                    'id': doc['id'],
                    'filename': doc['filename'],
                    'tags': tags_str,
                    'similarity': similarity_value
                })
                
                self.logger.debug(f"Document {doc['id']} similarity: {similarity_value}%")
            else:
                self.logger.warning(f"Document {doc['id']} has no embedding")
        
        # Sort documents by similarity (highest first)
        documents = sorted(documents, key=lambda x: x.get('similarity', 0), reverse=True)
        
        # Sort similarity info for tag suggestions
        doc_similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Get diverse tag suggestions
        tag_suggestions = self._get_diverse_tag_suggestions(doc_similarities)
        
        self.logger.info(f"Calculated {len(similarity_data)} similarities and found {len(tag_suggestions)} tag suggestions")
        
        return similarity_data, documents, tag_suggestions
    
    def generate_embedding(self, text):
        """
        Generate embedding for text using BERT
        
        Args:
            text (str): Text to generate embedding for
            
        Returns:
            list: Embedding vector as a list
        """
        if self.model is None:
            self.logger.warning("Embedding model not loaded, returning empty embedding")
            return []
        
        try:
            # Generate embedding
            embedding = self.model.encode(text)
            # Convert to list for JSON serialization
            embedding_list = embedding.tolist()
            self.logger.debug(f"Generated embedding of dimension {len(embedding_list)}")
            return embedding_list
        except Exception as e:
            self.logger.error(f"Error generating embedding: {str(e)}")
            return []
    
    def compute_similarity(self, embedding1, embedding2):
        """
        Compute cosine similarity between two embeddings with better error handling
        
        Args:
            embedding1 (list): First embedding
            embedding2 (list): Second embedding
            
        Returns:
            float: Cosine similarity
        """
        self.logger.debug(f"Computing similarity between embeddings of lengths {len(embedding1)} and {len(embedding2)}")
        
        # Basic validation
        if not embedding1 or not embedding2:
            self.logger.warning("Empty embedding detected")
            return 0
        
        if len(embedding1) != len(embedding2):
            self.logger.warning(f"Embedding dimension mismatch: {len(embedding1)} vs {len(embedding2)}")
            # If dimensions don't match, we have to return 0
            return 0
        
        try:
            # Convert to numpy arrays
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Compute cosine similarity
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                self.logger.warning("Zero vector detected")
                return 0
                
            similarity = np.dot(vec1, vec2) / (norm1 * norm2)
            self.logger.debug(f"Computed similarity: {similarity}")
            return similarity
            
        except Exception as e:
            self.logger.error(f"Error computing similarity: {str(e)}")
            return 0
    
    def _get_diverse_tag_suggestions(self, sorted_similarities, threshold=30, max_suggestions=3):
        """
        Get diverse tag suggestions from sorted similarities
        
        Args:
            sorted_similarities (list): List of documents with similarity scores, sorted by similarity
            threshold (int): Minimum similarity threshold (percentage)
            max_suggestions (int): Maximum number of suggestions to return
            
        Returns:
            list: List of diverse tag suggestions
        """
        # Get documents for tag suggestions with threshold
        potential_suggestions = [doc for doc in sorted_similarities if doc['similarity'] > threshold]
        
        # Track unique tag sets to ensure diversity
        unique_tag_sets = set()
        diverse_suggestions = []
        
        # Filter to include only diverse tag sets
        for doc in potential_suggestions:
            # Get tags as a list
            if isinstance(doc['tags'], str):
                tags = [tag.strip() for tag in doc['tags'].split(',')]
            else:
                tags = doc['tags']
            
            # Normalize tags by sorting
            normalized_tags = ','.join(sorted(tags))
            
            if normalized_tags not in unique_tag_sets:
                unique_tag_sets.add(normalized_tags)
                diverse_suggestions.append(doc)
            
            # Stop after finding max_suggestions diverse suggestions
            if len(diverse_suggestions) >= max_suggestions:
                break
        
        return diverse_suggestions