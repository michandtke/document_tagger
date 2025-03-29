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
    
    # routes/main.py (update the get function)
    @rt('/')
    def get():
        """Main page route - list all documents"""
        # Get all documents
        documents = document_service.get_all_documents()
        logger.info(f"Displaying {len(documents)} documents on main page")
        
        # Create UI components
        upload_section = UIComponents.create_upload_section()
        new_file_section = UIComponents.create_new_file_section()
        search_section = UIComponents.create_search_section()
        doc_table = UIComponents.create_document_table(documents)
        
        # Add navigation links
        nav_links = Div(
            A("View Raw Files", href="/raw_files", cls="nav-link"),
            cls="container nav-container"
        )
        
        # Render page
        return Titled(
            "Document Tagger System",
            Style(Styles.get_app_css()),
            Script(Scripts.get_client_js()),
            upload_section,
            new_file_section,
            search_section,
            nav_links,
            Div(doc_table, cls="container")
        )