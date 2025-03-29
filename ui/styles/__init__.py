# UI Styles module
# This file aggregates all the styles from different modules

from ui.styles.common.base import get_base_css
from ui.styles.documents.document_list import get_document_list_css
from ui.styles.raw_documents.raw_files import get_raw_files_css
from ui.styles.metadata.metadata_form import get_metadata_form_css

class Styles:
    """
    Class for accessing application styles
    """
    
    @staticmethod
    def get_app_css():
        """
        Get the complete application CSS
        
        Returns:
            str: Complete application CSS
        """
        # Combine all CSS styles
        return "\n".join([
            get_base_css(),
            get_document_list_css(),
            get_raw_files_css(),
            get_metadata_form_css()
        ])
    
    @staticmethod
    def get_base_css():
        """
        Get base CSS styles
        
        Returns:
            str: Base CSS styles
        """
        return get_base_css()
    
    @staticmethod
    def get_documents_css():
        """
        Get CSS for document pages
        
        Returns:
            str: Document pages CSS
        """
        return "\n".join([
            get_base_css(),
            get_document_list_css()
        ])
    
    @staticmethod
    def get_raw_files_css():
        """
        Get CSS for raw files pages
        
        Returns:
            str: Raw files pages CSS
        """
        return "\n".join([
            get_base_css(),
            get_raw_files_css()
        ])
    
    @staticmethod
    def get_metadata_css():
        """
        Get CSS for metadata form pages
        
        Returns:
            str: Metadata form pages CSS
        """
        return "\n".join([
            get_base_css(),
            get_metadata_form_css()
        ])
