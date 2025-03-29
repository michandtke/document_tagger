import logging

class DocumentService:
    """
    Service for document operations
    """
    
    def __init__(self, webdav_service):
        """
        Initialize document service
        
        Args:
            webdav_service: WebDAV service for storage
        """
        self.webdav = webdav_service
        self.logger = logging.getLogger(__name__)
    
    def get_all_documents(self):
        """
        Get all documents from storage
        
        Returns:
            list: List of document dictionaries
        """
        self.logger.info("Fetching all documents")
        try:
            # Uses the cached version if available
            documents = self.webdav.get_all_documents()
            self.logger.debug(f"Retrieved {len(documents)} documents")
            return documents
        except Exception as e:
            self.logger.error(f"Error fetching documents: {str(e)}")
            return []
    
    def add_document(self, filename, tags, file_data=None, text_content=None):
        """
        Add a document with metadata
        
        Args:
            filename (str): Document filename
            tags (str): Comma-separated tags
            file_data (bytes, optional): File binary data
            text_content (str, optional): Extracted text for embedding
            
        Returns:
            bool: Success status
        """
        self.logger.info(f"Adding document: {filename}")
        
        try:
            # Use the webdav service to add the document
            # This will also update the cache
            success = self.webdav.add_document(
                filename=filename,
                tags=tags,
                file_data=file_data,
                content=text_content
            )
            
            if success:
                self.logger.info(f"Successfully added document: {filename}")
            else:
                self.logger.error(f"Failed to add document: {filename}")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Error adding document {filename}: {str(e)}")
            return False
    
    def delete_document(self, doc_id):
        """
        Delete a document and its metadata
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            bool: Success status
        """
        self.logger.info(f"Deleting document: {doc_id}")
        
        try:
            # This will also update the cache
            success = self.webdav.delete_document(doc_id)
            
            if success:
                self.logger.info(f"Successfully deleted document: {doc_id}")
            else:
                self.logger.error(f"Failed to delete document: {doc_id}")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Error deleting document {doc_id}: {str(e)}")
            return False