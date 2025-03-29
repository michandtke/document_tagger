# UI Scripts module
# This file aggregates all the scripts from different modules

from ui.scripts.common.utils import get_utils_js
from ui.scripts.documents.upload_handler import get_upload_handler_js
from ui.scripts.raw_documents.table_handler import get_raw_files_table_js
from ui.scripts.metadata.file_preview import get_file_preview_js
from ui.scripts.metadata.metadata_handler import get_metadata_handler_js

class Scripts:
    """
    Class for accessing application scripts
    """

    @staticmethod
    def get_client_js():
        """
        Get the complete client-side JavaScript
        
        Returns:
            str: Complete client-side JavaScript
        """
        # Combine all JavaScript
        return "\n".join([
            get_utils_js(),
            get_upload_handler_js(),
            get_raw_files_table_js(),
            get_file_preview_js(),
            get_metadata_handler_js()
        ])
    
    @staticmethod
    def get_utils_js():
        """
        Get utility JavaScript functions
        
        Returns:
            str: Utility JavaScript
        """
        return get_utils_js()
    
    @staticmethod
    def get_documents_js():
        """
        Get JavaScript for document pages
        
        Returns:
            str: Document pages JavaScript
        """
        return "\n".join([
            get_utils_js(),
            get_upload_handler_js()
        ])
    
    @staticmethod
    def get_raw_files_js():
        """
        Get JavaScript for raw files pages
        
        Returns:
            str: Raw files pages JavaScript
        """
        return "\n".join([
            get_utils_js(),
            get_raw_files_table_js()
        ])
    
    @staticmethod
    def get_metadata_js():
        """
        Get JavaScript for metadata form pages
        
        Returns:
            str: Metadata form pages JavaScript
        """
        return "\n".join([
            get_utils_js(),
            get_file_preview_js(),
            get_metadata_handler_js()
        ])