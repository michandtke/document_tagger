import logging
from fasthtml.common import *
from starlette.responses import RedirectResponse, JSONResponse
from . import document_service, similarity_service
from ui.components import UIComponents
from ui.styles import Styles
from ui.scripts import Scripts

logger = logging.getLogger(__name__)

def register_routes(app):
    """Register search-related routes"""
    rt = app.route
    
    @rt('/search')
    async def get(request):
        """Search route with embedding similarity calculation"""
        # Extract query parameter from the request
        query = request.query_params.get('query', '')
        
        if not query:
            return RedirectResponse('/', status_code=303)
        
        logger.info(f"Searching with query: {query}")
        
        # Use similarity service to calculate similarities
        similarity_data, sorted_documents, _ = similarity_service.calculate_similarities(query)
        
        # Create UI components
        upload_section = UIComponents.create_upload_section()
        new_file_section = UIComponents.create_new_file_section()
        search_section = UIComponents.create_search_section(query)
        doc_table = UIComponents.create_document_table(sorted_documents, similarity_data)
        
        # Add navigation
        nav_links = UIComponents.create_navigation([("Back to Document Library", "/")])
        
        # Add debug information
        debug_info = ""
        if similarity_data:
            debug_info = f"Found {len(similarity_data)} similarities."
        
        # Render search results page
        return Titled(
            f"Search: {query} - Document Tagger",
            Style(Styles.get_documents_css()),
            Script(Scripts.get_documents_js()),
            upload_section,
            new_file_section,
            search_section,
            nav_links,
            Div(doc_table, cls="container"),
            Div(
                P(f"Showing search results for: '{query}'", cls="search-info"),
                P(debug_info, cls="debug-info"),
                cls="container"
            )
        )
    
    @rt('/preview_similarity')
    async def post(request):
        """Calculate similarity for a selected file before upload"""
        form = await request.form()
        file = form.get('file')
        tags = form.get('tags', 'document')
        
        if not file or not hasattr(file, 'filename'):
            return JSONResponse({
                "similarities": {},
                "tag_suggestions": [],
                "error": "No file provided"
            })
        
        try:
            file_data = await file.read()
            filename = file.filename
            
            # Use similarity service to calculate similarities with text extraction
            similarity_data, _, tag_suggestions = similarity_service.calculate_similarities_from_file(
                file_data, filename, tags
            )
            
            # Get suggested tags string from the first suggestion if available
            suggested_tags = ""
            if tag_suggestions and len(tag_suggestions) > 0:
                best_suggestion = tag_suggestions[0]
                if 'tags' in best_suggestion:
                    suggested_tags = best_suggestion['tags']
            
            # Return results as JSON
            return JSONResponse({
                "similarities": similarity_data,
                "tag_suggestions": tag_suggestions,
                "suggested_tags": suggested_tags
            })
            
        except Exception as e:
            logger.error(f"Error calculating preview similarity: {str(e)}")
            return JSONResponse({
                "similarities": {},
                "tag_suggestions": [],
                "suggested_tags": "",
                "error": str(e)
            })