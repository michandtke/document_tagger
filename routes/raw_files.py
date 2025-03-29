# routes/raw_files.py

import os
import logging
from fasthtml.common import *
from starlette.responses import RedirectResponse, Response
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
        nav_links = UIComponents.create_navigation([("View Document Library", "/")])
        # Render page
        return Titled(
            "Raw Files Manager",
            Style(Styles.get_raw_files_css()),
            Script(Scripts.get_raw_files_js()),
            nav_links,
            upload_section,
            Div(file_table, cls="container")
        )
        
    @rt('/add_metadata_form')
    def get(request):
        """Dedicated page for adding metadata to a raw file"""
        # Get filename from query parameter
        filename = request.query_params.get('filename')
        
        if not filename:
            # Redirect to raw files page if no filename is provided
            return RedirectResponse('/raw_files', status_code=303)
        
        # Create metadata form
        metadata_form = UIComponents.create_metadata_form(filename)
        
        # Render page
        return Titled(
            f"Add Metadata - {filename}",
            Style(Styles.get_metadata_css()),
            Script(Scripts.get_metadata_js()),
            metadata_form
        )
    
    @rt('/raw_file_preview')
    async def get(request):
        """Stream the raw file for preview"""
        filename = request.query_params.get('filename')
        if not filename:
            return Response("Filename not provided", status_code=400)
        
        try:
            # Get raw file from WebDAV
            file_data = document_service.webdav.get_raw_document(filename)
            
            if file_data is None:
                logger.error(f"Error downloading raw document for preview: {filename}")
                return Response("Error downloading file", status_code=404)
            
            # Determine content type based on file extension
            ext = os.path.splitext(filename)[1].lower()
            content_type = None
            
            # Set appropriate content type based on file extension
            if ext in ['.jpg', '.jpeg']:
                content_type = 'image/jpeg'
            elif ext == '.png':
                content_type = 'image/png'
            elif ext == '.gif':
                content_type = 'image/gif'
            elif ext == '.pdf':
                content_type = 'application/pdf'
            elif ext in ['.doc', '.docx']:
                content_type = 'application/msword'
            elif ext in ['.xls', '.xlsx']:
                content_type = 'application/vnd.ms-excel'
            elif ext in ['.ppt', '.pptx']:
                content_type = 'application/vnd.ms-powerpoint'
            elif ext == '.txt':
                content_type = 'text/plain'
            elif ext == '.html':
                content_type = 'text/html'
            elif ext == '.css':
                content_type = 'text/css'
            elif ext == '.js':
                content_type = 'application/javascript'
            elif ext == '.json':
                content_type = 'application/json'
            elif ext == '.xml':
                content_type = 'application/xml'
            else:
                content_type = 'application/octet-stream'
            
            # Return the file data with the appropriate content type
            return Response(file_data, media_type=content_type)
            
        except Exception as e:
            logger.error(f"Error serving preview for {filename}: {str(e)}")
            return Response(f"Error: {str(e)}", status_code=500)
    
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