# UI Components module
# This file makes the components available through the ui.components package

# Import from common components
from ui.components.common.navigation import create_navigation

# Import from documents components
from ui.components.documents.document_table import create_document_table, format_tags
from ui.components.documents.upload_section import create_upload_section, create_new_file_section
from ui.components.documents.search_section import create_search_section, create_similarity_table

# Import from raw_documents components
from ui.components.raw_documents.raw_files_table import create_raw_files_table

# Import from metadata components
from ui.components.metadata.metadata_form import create_metadata_form

# Create a UIComponents class that has all components as static methods for backward compatibility
class UIComponents:
    @staticmethod
    def create_navigation(*args, **kwargs):
        return create_navigation(*args, **kwargs)
        
    @staticmethod
    def format_tags(*args, **kwargs):
        return format_tags(*args, **kwargs)
        
    @staticmethod
    def create_document_table(*args, **kwargs):
        return create_document_table(*args, **kwargs)
        
    @staticmethod
    def create_upload_section(*args, **kwargs):
        return create_upload_section(*args, **kwargs)
        
    @staticmethod
    def create_new_file_section(*args, **kwargs):
        return create_new_file_section(*args, **kwargs)
        
    @staticmethod
    def create_search_section(*args, **kwargs):
        return create_search_section(*args, **kwargs)
        
    @staticmethod
    def create_similarity_table(*args, **kwargs):
        return create_similarity_table(*args, **kwargs)
        
    @staticmethod
    def create_raw_files_table(*args, **kwargs):
        return create_raw_files_table(*args, **kwargs)
        
    @staticmethod
    def create_metadata_form(*args, **kwargs):
        return create_metadata_form(*args, **kwargs)