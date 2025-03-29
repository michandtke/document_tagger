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
        nav_links = Div(
            A("View Document Library", href="/", cls="nav-link"),
            cls="container nav-container"
        )
        
        # Include custom script to enhance showMetadataForm to auto-suggest tags and show file preview
        custom_script = Script("""
        // Enhanced showMetadataForm function to automatically suggest tags and show file preview
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
            
            // Display file preview
            const previewContainer = document.getElementById('file-preview-container');
            if (previewContainer) {
                previewContainer.innerHTML = '<div class="loading">Loading file preview...</div>';
                await loadFilePreview(filename, previewContainer);
            }
            
            // Calculate similarities and get tag suggestions
            getFileSimilarities(filename);
            
            // Scroll to the metadata form
            metadataForm.scrollIntoView({ behavior: 'smooth' });
        }
        
        // Function to load file preview based on file type
        async function loadFilePreview(filename, container) {
            try {
                // Get the file extension
                const ext = filename.split('.').pop().toLowerCase();
                
                // Create a URL to stream the file content
                const previewUrl = '/raw_file_preview?filename=' + encodeURIComponent(filename);
                
                // Display preview based on file type
                if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'].includes(ext)) {
                    // Image preview
                    container.innerHTML = `<img src="${previewUrl}" alt="${filename}" />`;
                } 
                else if (ext === 'pdf') {
                    // PDF preview using iframe
                    container.innerHTML = `<iframe class="pdf-preview" src="${previewUrl}" title="${filename}"></iframe>`;
                }
                else if (['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'].includes(ext)) {
                    // Office document icon
                    const docType = {
                        'doc': 'Word', 'docx': 'Word',
                        'xls': 'Excel', 'xlsx': 'Excel',
                        'ppt': 'PowerPoint', 'pptx': 'PowerPoint'
                    }[ext];
                    
                    container.innerHTML = `
                        <div class="unsupported-file">
                            <div class="document-icon">📄</div>
                            <div>${docType} Document</div>
                            <div class="file-info">${filename}</div>
                        </div>
                    `;
                }
                else if (['txt', 'csv', 'json', 'xml', 'html', 'css', 'js'].includes(ext)) {
                    // Try to fetch and display text content
                    try {
                        const response = await fetch(previewUrl);
                        if (response.ok) {
                            const text = await response.text();
                            container.innerHTML = `<pre style="white-space: pre-wrap; max-height: 300px; overflow: auto;">${text.substring(0, 5000)}</pre>`;
                            if (text.length > 5000) {
                                container.innerHTML += '<div class="file-info">(Preview truncated, showing first 5000 characters)</div>';
                            }
                        } else {
                            throw new Error('Failed to load text content');
                        }
                    } catch (e) {
                        container.innerHTML = `
                            <div class="unsupported-file">
                                <div class="document-icon">📄</div>
                                <div>Text Document</div>
                                <div class="file-info">${filename}</div>
                            </div>
                        `;
                    }
                }
                else {
                    // Generic file icon for unsupported types
                    container.innerHTML = `
                        <div class="unsupported-file">
                            <div class="document-icon">📄</div>
                            <div>File Preview Not Available</div>
                            <div class="file-info">${filename}</div>
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Error loading file preview:', error);
                container.innerHTML = `
                    <div class="unsupported-file">
                        <div class="document-icon">❌</div>
                        <div>Error Loading Preview</div>
                        <div class="file-info">${error.message}</div>
                    </div>
                `;
            }
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