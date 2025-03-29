import os
import logging
import threading
import time
from typing import Dict, List, Optional, Any

class DocumentCache:
    """
    Cache for WebDAV documents to avoid reloading all files on every request.
    
    This maintains an in-memory cache of documents and their metadata,
    and only reloads from WebDAV when documents are modified or added.
    """
    
    def __init__(self):
        """Initialize the document cache"""
        self.logger = logging.getLogger(__name__)
        self.documents = {}  # Document cache: {id: document_dict}
        self.is_loaded = False  # Flag to track if initial load has happened
        self.lock = threading.RLock()  # Thread-safe lock for cache operations
        self.last_reload_time = 0  # Track when cache was last reloaded
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Get all documents from the cache
        
        Returns:
            list: List of document dictionaries
        """
        with self.lock:
            # Return a copy of the values to prevent modification of cache entries
            return list(self.documents.values())
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document from the cache by ID
        
        Args:
            doc_id: Document ID
            
        Returns:
            dict: Document dictionary or None if not found
        """
        with self.lock:
            return self.documents.get(doc_id)
    
    def update_document(self, document: Dict[str, Any]) -> None:
        """
        Update or add a document in the cache
        
        Args:
            document: Document dictionary
        """
        if not document or 'id' not in document:
            self.logger.warning("Attempted to update document with missing ID")
            return
            
        with self.lock:
            doc_id = document['id']
            self.documents[doc_id] = document
            self.logger.debug(f"Updated document in cache: {doc_id}")
    
    def delete_document(self, doc_id: str) -> None:
        """
        Delete a document from the cache
        
        Args:
            doc_id: Document ID
        """
        with self.lock:
            if doc_id in self.documents:
                del self.documents[doc_id]
                self.logger.debug(f"Deleted document from cache: {doc_id}")
    
    def set_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Set the entire document cache (used for initial load)
        
        Args:
            documents: List of document dictionaries
        """
        with self.lock:
            # Clear existing documents
            self.documents = {}
            
            # Add new documents to cache
            for doc in documents:
                if 'id' in doc:
                    self.documents[doc['id']] = doc
                else:
                    self.logger.warning(f"Skipping document with missing ID: {doc}")
            
            self.is_loaded = True
            self.last_reload_time = time.time()
            self.logger.info(f"Loaded {len(self.documents)} documents into cache")
    
    def clear(self) -> None:
        """Clear the entire cache"""
        with self.lock:
            self.documents = {}
            self.is_loaded = False
            self.logger.info("Document cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self.lock:
            stats = {
                "document_count": len(self.documents),
                "is_loaded": self.is_loaded,
                "last_reload": time.strftime("%Y-%m-%d %H:%M:%S", 
                                            time.localtime(self.last_reload_time)) if self.last_reload_time else "Never"
            }
            return stats