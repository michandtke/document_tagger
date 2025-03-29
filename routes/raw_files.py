# routes/raw_files.py

import logging
from fasthtml.common import *
from starlette.responses import RedirectResponse
from . import document_service, similarity_service
from services.text_extraction import TextExtractor
from ui.components import UIComponents
from ui.styles import Styles
from ui.scripts import Scripts
from config import webdav_config
import requests

logger = logging.getLogger(__name__)
text_extractor = TextExtractor()

def register_routes(app):
    """Register raw files routes"""
    rt = app.route
    
    @rt('/raw_files')
    def get():
        """Raw files page - list all files without metadata"""
        # Get raw files folder from config
        raw_folder = webdav_config.get('raw_folder', '/raw_documents')
        
        # Get all files without metadata
        raw_files = document_service.webdav.get_all_files_without_metadata(raw_folder)
        
        # Create UI components
        upload_section = UIComponents.create_upload_section(target_folder=raw_folder)
        file_table = UIComponents.create_raw_files_table(raw_files)
        
        # Add navigation links
        nav_links = Div(
            A("View Document Library", href="/", cls="nav-link"),
            cls="container nav-container"
        )
        
        # Include custom script to enhance showMetadataForm to auto-suggest tags
        custom_script = Script("""
        // Enhanced showMetadataForm function to automatically suggest tags
        async function showMetadataForm(filename) {
            // Show the metadata form
            const metadataForm = document.getElementById('metadata-form');
            if (metadataForm) {
                metadataForm.classList.remove('hidden');
            }
            
            // Set the filename in the form
            const filenameSpan = document.getElementById('metadata-filename');
            const filenameInput = document.getElementById('filename-input');
            if (filenameSpan) filenameSpan.textContent = filename;
            if (filenameInput) filenameInput.value = filename;
            
            // Clear existing tag suggestions
            const suggestionsContainer = document.getElementById('tag-suggestions-container');
            if (suggestionsContainer) suggestionsContainer.innerHTML = '';
            
            // Show loading indicator
            const extractedTextPreview = document.getElementById('extracted-text-preview');
            if (extractedTextPreview) {
                extractedTextPreview.innerHTML = '<div class="loading">Analyzing file content...</div>';
            }
            
            // Calculate similarities and get tag suggestions
            getFileSimilarities(filename);
            
            // Scroll to the metadata form
            metadataForm.scrollIntoView({ behavior: 'smooth' });
        }
        """)
        
        # Render page
        return Titled(
            "Raw Files Manager",
            Style(Styles.get_app_css()),
            Script(Scripts.get_client_js()),
            custom_script,
            nav_links,
            upload_section,
            Div(file_table, cls="container")
        )
    
    @rt('/preview_raw_similarity')
    async def post(request):
        """Calculate similarity for a raw file before adding metadata"""
        form = await request.form()
        filename = form.get('filename')
        raw_folder = webdav_config.get('raw_folder', '/raw_documents')
        
        if not filename:
            return JSONResponse({
                "similarities": {},
                "tag_suggestions": [],
                "error": "No filename provided"
            })
        
        try:
            file_data = document_service.webdav.get_raw_document(filename)

            if file_data is None:
                logger.error(f"Error downloading raw document {filename}")
                return JSONResponse({
                    "similarities": {},
                    "tag_suggestions": [],
                    "error": f"Error downloading raw document {filename}"
                })
            
            # Extract text from file
            extracted_text = text_extractor.extract_text(file_data, filename)
            
            # Calculate similarities with existing documents
            similarity_data, _, tag_suggestions = similarity_service.calculate_similarities_from_file(
                file_data, filename, ""
            )
            
            # Get suggested tags string from the first suggestion if available
            suggested_tags = ""
            if tag_suggestions and len(tag_suggestions) > 0:
                best_suggestion = tag_suggestions[0]
                if 'tags' in best_suggestion:
                    suggested_tags = best_suggestion['tags']
            
            # Return similarities and tag suggestions
            return JSONResponse({
                "similarities": similarity_data,
                "tag_suggestions": tag_suggestions,
                "suggested_tags": suggested_tags,
                "extracted_text_sample": extracted_text[:500] if extracted_text else ""
            })
            
        except Exception as e:
            logger.error(f"Error calculating preview similarity: {str(e)}")
            return JSONResponse({
                "similarities": {},
                "tag_suggestions": [],
                "error": str(e)
            })
    
    @rt('/add_metadata')
    async def post(request):
        """Add metadata to a raw file and move it to the documents folder"""
        form = await request.form()
        filename = form.get('filename')
        tags = form.get('tags', 'document')
        raw_folder = webdav_config.get('raw_folder', '/raw_documents')
        
        if not filename:
            return RedirectResponse('/raw_files', status_code=303)
        
        try:
            file_data = document_service.webdav.get_raw_document(filename)

            if file_data is None:
                logger.error(f"Error downloading raw document {filename}")
                return Titled("Metadata Error", 
                             Div(f"Error downloading raw document {filename}", 
                                cls="container error"))
            
            # Extract text for embedding
            extracted_text = text_extractor.extract_text(file_data, filename)
            
            # Move file with metadata
            success = document_service.webdav.move_file_with_metadata(
                filename=filename,
                tags=tags,
                content=extracted_text
            )
            
            if success:
                logger.info(f"Successfully moved file {filename} with metadata")
                return RedirectResponse('/raw_files', status_code=303)
            else:
                logger.error(f"Failed to move file {filename}")
                return Titled("Metadata Error", 
                             Div("Failed to move file with metadata", cls="container error"))
                
        except Exception as e:
            logger.error(f"Error adding metadata: {str(e)}")
            return Titled("Metadata Error", Div(f"Error: {str(e)}", cls="container error"))