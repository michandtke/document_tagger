import logging
from fasthtml.common import *
from . import document_service, similarity_service
from ui.components import UIComponents
from ui.styles import Styles
from ui.scripts import Scripts

logger = logging.getLogger(__name__)

def register_routes(app):
    """Register main page routes"""
    rt = app.route
    
    @rt('/')
    def get(request):
        """Main page route - list all documents"""
        # Check if this is the initial page load or a non-HTMX request
        is_initial_load = not request.headers.get('HX-Request')
        
        # Get all documents
        documents = document_service.get_all_documents()
        logger.info(f"Displaying {len(documents)} documents on main page")
        
        # Create UI components
        upload_section = UIComponents.create_upload_section()
        new_file_section = UIComponents.create_new_file_section()
        search_section = UIComponents.create_search_section()
        doc_table = UIComponents.create_document_table(documents)
        
        # Add navigation links with links to other sections
        nav_links = UIComponents.create_navigation([
            ("View Raw Files", "/raw_files"),
            ("Admin Dashboard", "/admin")
        ])
        
        # Render page
        return Titled(
            "Document Tagger System",
            Style(Styles.get_documents_css()),
            Script(Scripts.get_documents_js()),
            upload_section,
            new_file_section,
            search_section,
            nav_links,
            Div(doc_table, cls="container")
        )