import os
import json
import logging
import requests
import datetime
from urllib.parse import urljoin, unquote
from services.document_cache import DocumentCache

class WebDAVService:
    """
    Service for WebDAV storage operations
    """
    
    def __init__(self, webdav_url, webdav_username, webdav_password, folder_path, folder_path_raw):
        """
        Initialize the WebDAV service
        
        Args:
            webdav_url (str): WebDAV server URL
            webdav_username (str): WebDAV username
            webdav_password (str): WebDAV password
            folder_path (str): Path to the folder for documents
            folder_path_raw (str): Path to the folder for raw documents
        """
        self.webdav_url = webdav_url
        self.auth = (webdav_username, webdav_password)
        self.folder_path = folder_path.strip('/')
        self.folder_path_raw = folder_path_raw.strip('/')
        self.base_url = urljoin(self.webdav_url, self.folder_path)
        self.base_url_raw = urljoin(self.webdav_url, self.folder_path_raw)
        self.logger = logging.getLogger(__name__)
        
        # Initialize document cache
        self.cache = DocumentCache()
        
        self.logger.info(f"Initializing WebDAV service with base URL: {self.base_url}")
        
        # Create folder if it doesn't exist
        try:
            self._check_or_create_folder()
        except Exception as e:
            self.logger.error(f"Error initializing WebDAV folder: {str(e)}")
    
    def _check_or_create_folder(self):
        """Create the base folder if it doesn't exist"""
        response = requests.request(
            "PROPFIND", 
            self.base_url, 
            auth=self.auth, 
            headers={"Depth": "0"},
            timeout=10
        )
        
        if response.status_code == 404:
            self.logger.info(f"Creating folder: {self.folder_path}")
            response = requests.request("MKCOL", self.base_url, auth=self.auth)
            if response.status_code >= 400:
                self.logger.error(f"Failed to create folder: {response.status_code}")
        elif response.status_code >= 400:
            self.logger.error(f"Error checking folder: {response.status_code}")
    
    def _get_file_url(self, filename):
        """Get the full URL for a file"""
        encoded_filename = requests.utils.quote(filename)
        return urljoin(self.base_url + '/', encoded_filename)
    
    def _get_file_url_raw_folder(self, filename):
        """Get the full URL for a file"""
        encoded_filename = requests.utils.quote(filename)
        return urljoin(self.base_url_raw + '/', encoded_filename)
    
    def get_all_documents(self):
        """
        Get all documents from WebDAV storage with caching
        
        Returns:
            list: List of document dictionaries
        """
        # If cache is already loaded, return cached documents
        if self.cache.is_loaded:
            self.logger.info("Using cached documents")
            return self.cache.get_all_documents()
            
        self.logger.info(f"Loading documents from WebDAV folder: {self.base_url}")
        
        # List files
        files = self._list_files()
        
        # Find document and metadata pairs
        documents = []
        metadata_files = [f for f in files if f.endswith('.metadata.json')]
        
        self.logger.info(f"Found {len(metadata_files)} metadata files")
        
        # Process each metadata file to get document info
        for metadata_file in metadata_files:
            # Get the corresponding document filename
            doc_file = metadata_file.replace(".metadata.json", "")
            
            # Skip if the document doesn't exist in the file list
            if doc_file not in files:
                self.logger.warning(f"Metadata exists but document missing: {doc_file}")
                continue
                
            # Read metadata
            metadata = self.read_metadata(metadata_file)
            
            # Create document info
            documents.append({
                'id': doc_file,  # Use filename as ID
                'filename': doc_file,
                'tags': metadata.get('tags', []),
                'embedding': metadata.get('embedding', []),
                'similarity': 0  # Default value, will be calculated when needed
            })
        
        # Update the cache with all documents
        self.cache.set_documents(documents)
        
        self.logger.info(f"Retrieved {len(documents)} documents with metadata")
        return documents
    
    def _list_files(self):
        """
        List files in the WebDAV folder
        
        Returns:
            list: List of filenames
        """
        try:
            # Send PROPFIND request to list files
            response = requests.request(
                "PROPFIND", 
                self.base_url, 
                auth=self.auth, 
                headers={"Depth": "1"},
                timeout=15
            )
            
            self.logger.debug(f"PROPFIND response status: {response.status_code}")
            
            if response.status_code >= 400:
                self.logger.error(f"Error listing files: {response.status_code}")
                return []
            
            # Simple parsing of XML response to get filenames
            content = response.text
            files = []
            
            # Extract hrefs from the XML
            import re
            href_pattern = r'<[^>]*?href[^>]*?>(.*?)</[^>]*?href[^>]*?>'
            
            matches = re.findall(href_pattern, content, re.IGNORECASE | re.DOTALL)
            
            for href in matches:
                # Clean up the href
                href = href.strip()
                
                # Skip the folder itself and other folders
                if href.rstrip('/') == self.base_url.rstrip('/') or href.endswith('/'):
                    continue
                
                # Extract filename from the URL
                filename = os.path.basename(href)
                if filename:
                    # URL decode the filename
                    try:
                        filename = unquote(filename)
                        files.append(filename)
                    except Exception as e:
                        self.logger.error(f"Error decoding filename: {e}")
            
            self.logger.debug(f"Found {len(files)} files")
            return files
            
        except Exception as e:
            self.logger.error(f"Error listing files: {str(e)}")
            return []
    
    def read_metadata(self, metadata_filename):
        """
        Read metadata from a .metadata.json file
        
        Args:
            metadata_filename (str): Filename of the metadata file
            
        Returns:
            dict: Metadata as a dictionary
        """
        self.logger.debug(f"Reading metadata from {metadata_filename}")
        metadata_url = self._get_file_url(metadata_filename)
        
        try:
            response = requests.get(metadata_url, auth=self.auth, timeout=10)
            
            if response.status_code >= 400:
                self.logger.error(f"Error downloading metadata: {response.status_code}")
                return {"tags": [], "embedding": []}
            
            try:
                metadata = response.json()
                return metadata
            except json.JSONDecodeError as e:
                self.logger.error(f"Error parsing metadata JSON: {str(e)}")
                return {"tags": [], "embedding": []}
                
        except Exception as e:
            self.logger.error(f"Error reading metadata from {metadata_filename}: {str(e)}")
            return {"tags": [], "embedding": []}
        
    def get_raw_document(self, filename):
        """
        Read file from raw documents folder
        
        Args:
            filename (str): Filename to read
            
        Returns:
            bytes: Filedata as bytes
        """
        self.logger.debug(f"Reading file from {self.folder_path_raw}: {filename}")
        raw_file_url = self._get_file_url_raw_folder(filename)
        
        try:
            response = requests.get(raw_file_url, auth=self.auth, timeout=10)
            
            if response.status_code >= 400:
                self.logger.error(f"Error downloading raw file ({raw_file_url}): {response.status_code}")
                return
            return response.content
                
        except Exception as e:
            self.logger.error(f"Error downloading raw file ({raw_file_url}): {str(e)}")
            return
    
    def add_document(self, filename, tags, file_data=None, content=None):
        """
        Add a document with metadata to WebDAV
        
        Args:
            filename (str): Name of the document
            tags (str): Comma-separated tags
            file_data (bytes, optional): Binary file data
            content (str, optional): Text content for embedding
            
        Returns:
            bool: Success status
        """
        self.logger.info(f"Adding document: {filename} with tags: {tags}")
        
        # Convert tags string to list
        tag_list = [tag.strip() for tag in tags.split(',')]
        
        # Create metadata
        metadata = {
            "tags": tag_list,
            "embedding": [],  # Will be updated if content is provided
            "upload_date": datetime.datetime.now().isoformat()
        }
        
        # Add embedding if content is provided
        if content:
            try:
                from services.similarity_service import SimilarityService
                # Create a temporary service just for embedding generation
                temp_service = SimilarityService(None)
                embedding = temp_service.generate_embedding(content)
                metadata["embedding"] = embedding
                self.logger.info(f"Generated embedding with {len(embedding)} dimensions")
            except Exception as e:
                self.logger.error(f"Error generating embedding: {str(e)}")
        
        # Create document on WebDAV
        doc_url = self._get_file_url(filename)
        metadata_url = self._get_file_url(f"{filename}.metadata.json")
        
        # Upload document
        doc_content = file_data if file_data is not None else content.encode('utf-8') if content else b"Empty document"
        success = True
        
        try:
            response = requests.put(doc_url, data=doc_content, auth=self.auth, timeout=30)
            if response.status_code >= 400:
                self.logger.error(f"Error uploading document: {response.status_code}")
                success = False
            else:
                self.logger.debug(f"Document uploaded successfully")
        except Exception as e:
            self.logger.error(f"Error uploading document: {str(e)}")
            success = False
        
        # Upload metadata
        try:
            metadata_json = json.dumps(metadata)
            response = requests.put(metadata_url, data=metadata_json, auth=self.auth, timeout=10)
            if response.status_code >= 400:
                self.logger.error(f"Error uploading metadata: {response.status_code}")
                success = False
            else:
                self.logger.debug(f"Metadata uploaded successfully")
        except Exception as e:
            self.logger.error(f"Error uploading metadata: {str(e)}")
            success = False
        
        # If successful, update the document cache
        if success:
            # Create document object
            doc = {
                'id': filename,
                'filename': filename,
                'tags': tag_list,
                'embedding': metadata.get('embedding', []),
                'similarity': 0
            }
            # Update cache
            self.cache.update_document(doc)
        
        return success
    
    def delete_document(self, doc_id):
        """
        Delete a document and its metadata from WebDAV
        
        Args:
            doc_id (str): Document ID (filename)
            
        Returns:
            bool: Success status
        """
        self.logger.info(f"Deleting document: {doc_id}")
        doc_url = self._get_file_url(doc_id)
        metadata_url = self._get_file_url(f"{doc_id}.metadata.json")
        
        success = True
        
        # Delete document
        try:
            response = requests.delete(doc_url, auth=self.auth, timeout=10)
            if response.status_code >= 400 and response.status_code != 404:
                self.logger.error(f"Error deleting document: {response.status_code}")
                success = False
            else:
                self.logger.debug(f"Document deleted successfully")
        except Exception as e:
            self.logger.error(f"Error deleting document: {str(e)}")
            success = False
        
        # Delete metadata
        try:
            response = requests.delete(metadata_url, auth=self.auth, timeout=10)
            if response.status_code >= 400 and response.status_code != 404:
                self.logger.error(f"Error deleting metadata: {response.status_code}")
                success = False
            else:
                self.logger.debug(f"Metadata deleted successfully")
        except Exception as e:
            self.logger.error(f"Error deleting metadata: {str(e)}")
            success = False
        
        # Update the cache if the deletion was successful
        if success:
            self.cache.delete_document(doc_id)
        
        return success
    
    def get_all_files_without_metadata(self, raw_folder):
        """
        Get all files from a folder that don't have metadata
        
        Args:
            raw_folder (str): Path to folder with raw files
            
        Returns:
            list: List of file dictionaries
        """
        self.logger.info(f"Listing files in raw folder: {raw_folder}")
        
        # List files
        files = self._list_files_in_folder(raw_folder)
        
        # Create file info
        file_list = []
        for filename in files:
            # Skip metadata files
            if filename.endswith('.metadata.json'):
                continue
                
            # Check if there's a metadata file
            metadata_file = f"{filename}.metadata.json"
            if metadata_file in files:
                # Skip files that already have metadata
                continue
                
            # Add file without metadata to the list
            file_list.append({
                'id': filename,
                'filename': filename,
                'path': os.path.join(raw_folder, filename).replace('\\', '/')
            })
        
        self.logger.info(f"Found {len(file_list)} files without metadata")
        return file_list
        
    def _list_files_in_folder(self, folder_path):
        """
        List files in a specific WebDAV folder
        
        Args:
            folder_path (str): Path to folder
            
        Returns:
            list: List of filenames
        """
        folder_url = urljoin(self.webdav_url, folder_path.strip('/'))
        
        try:
            # Send PROPFIND request to list files
            response = requests.request(
                "PROPFIND", 
                folder_url, 
                auth=self.auth, 
                headers={"Depth": "1"},
                timeout=15
            )
            
            self.logger.debug(f"PROPFIND response status: {response.status_code}")
            
            if response.status_code >= 400:
                self.logger.error(f"Error listing files: {response.status_code}")
                return []
            
            # Simple parsing of XML response to get filenames
            content = response.text
            files = []
            
            # Extract hrefs from the XML
            import re
            href_pattern = r'<[^>]*?href[^>]*?>(.*?)</[^>]*?href[^>]*?>'
            
            matches = re.findall(href_pattern, content, re.IGNORECASE | re.DOTALL)
            
            for href in matches:
                # Clean up the href
                href = href.strip()
                
                # Skip the folder itself and other folders
                if href.rstrip('/') == folder_url.rstrip('/') or href.endswith('/'):
                    continue
                
                # Extract filename from the URL
                filename = os.path.basename(href)
                if filename:
                    # URL decode the filename
                    try:
                        filename = unquote(filename)
                        files.append(filename)
                    except Exception as e:
                        self.logger.error(f"Error decoding filename: {e}")
            
            self.logger.debug(f"Found {len(files)} files in {folder_path}")
            return files
            
        except Exception as e:
            self.logger.error(f"Error listing files in {folder_path}: {str(e)}")
            return []

    def move_file_with_metadata(self, filename, tags, content=None):
        """
        Move a file from raw documents folder to the documents folder and add metadata
        
        Args:
            filename (str): Filename (will be used in target folder)
            tags (str): Comma-separated tags
            content (str, optional): Text content for embedding
            
        Returns:
            bool: Success status
        """
        self.logger.info(f"Moving file {filename} from raw documents to documents folder with tags: {tags}")
        
        try:
            # Download the file
            source_url = self._get_file_url_raw_folder(filename)
            response = requests.get(source_url, auth=self.auth, timeout=30)
            
            if response.status_code >= 400:
                self.logger.error(f"Error downloading source file: {response.status_code}")
                return False
            
            file_data = response.content
            
            # Add the file to documents folder with metadata
            success = self.add_document(filename, tags, file_data, content)
            
            if success:
                # Delete the original file
                try:
                    delete_response = requests.delete(source_url, auth=self.auth, timeout=10)
                    if delete_response.status_code >= 400 and delete_response.status_code != 404:
                        self.logger.error(f"Error deleting source file: {delete_response.status_code}")
                except Exception as e:
                    self.logger.error(f"Error deleting source file: {str(e)}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error moving file: {str(e)}")
            return False
            
    def reload_cache(self):
        """
        Force a reload of the document cache
        
        Returns:
            int: Number of documents loaded
        """
        self.logger.info("Forcing reload of document cache")
        self.cache.clear()
        documents = self.get_all_documents()  # This will reload and update the cache
        return len(documents)
        
    def get_cache_stats(self):
        """
        Get document cache statistics
        
        Returns:
            dict: Cache statistics
        """
        return self.cache.get_stats()