import logging
from fasthtml.common import *
from starlette.responses import RedirectResponse
from . import document_service, similarity_service
from ui.components import UIComponents
from ui.styles import Styles
from ui.scripts import Scripts

logger = logging.getLogger(__name__)

def register_routes(app):
    """Register admin routes for managing cache and system settings"""
    rt = app.route
    
    @rt('/admin')
    def get():
        """Admin dashboard"""
        # Get document cache statistics
        doc_cache_stats = document_service.webdav.get_cache_stats()
        
        # Format document cache stats for display
        doc_stats_items = []
        for key, value in doc_cache_stats.items():
            doc_stats_items.append(Tr(Td(key.replace('_', ' ').title()), Td(str(value))))
        
        # Create document stats table
        doc_stats_table = Table(
            Tr(Th("Statistic"), Th("Value")),
            *doc_stats_items,
            cls="doc-table"
        )
        
        # Admin actions for document cache
        doc_cache_actions = Div(
            H3("Document Cache Management"),
            Button("Reload Document Cache", 
                   cls="delete-btn", 
                   onclick="if(confirm('Are you sure you want to reload the document cache?')) { window.location.href = '/admin/reload_doc_cache'; }"),
            style="margin-top: 20px;"
        )
        
        # Navigation links
        nav_links = UIComponents.create_navigation([("Back to Document Library", "/")])
        
        # Render admin page
        return Titled(
            "Admin Dashboard",
            Style(Styles.get_base_css()),
            Script(Scripts.get_utils_js()),
            nav_links,
            Div(
                H2("Document Cache Statistics"),
                doc_stats_table,
                doc_cache_actions,
                cls="container"
            )
        )
    
    @rt('/admin/reload_doc_cache')
    def get():
        """Reload the document cache"""
        try:
            num_docs = document_service.webdav.reload_cache()
            logger.info(f"Reloaded document cache with {num_docs} documents")
            
            # Redirect back to admin page
            return RedirectResponse('/admin', status_code=303)
        except Exception as e:
            logger.error(f"Error reloading document cache: {str(e)}")
            return Titled("Cache Error", 
                         Div(f"Error reloading document cache: {str(e)}", cls="container error"))