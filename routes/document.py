import logging
import datetime
from fasthtml.common import *
from starlette.responses import RedirectResponse, JSONResponse
from . import document_service, similarity_service
from services.text_extraction import TextExtractor
from ui.components import UIComponents

logger = logging.getLogger(__name__)

def register_routes(app):
    """Register document management routes"""
    rt = app.route
    
    @rt('/upload_document')
    async def post(request):
        """Upload a document to the WebDAV server"""
        form = await request.form()
        file = form.get('file')
        tags = form.get('tags', 'document')
        
        if not file or not hasattr(file, 'filename'):
            return RedirectResponse('/', status_code=303)
        
        try:
            filename = file.filename
            file_data = await file.read()
            
            logger.info(f"Uploading document: {filename}")
            
            # Extract text for embedding generation
            text_extractor = TextExtractor()
            extracted_text = text_extractor.extract_text(file_data, filename)
            logger.info(f"Extracted {len(extracted_text)} characters of text from {filename}")
            
            # Upload document with extracted text for embedding
            success = document_service.add_document(
                filename=filename,
                tags=tags,
                file_data=file_data,
                text_content=extracted_text
            )
            
            if success:
                logger.info(f"Successfully uploaded {filename}")
                return RedirectResponse('/', status_code=303)
            else:
                logger.error(f"Failed to upload {filename}")
                return Titled("Upload Error", 
                             Div("Failed to upload document", cls="container error"))
                
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            return Titled("Upload Error", Div(f"Error: {str(e)}", cls="container error"))
    
    @rt('/delete_document')
    async def post(request):
        """Delete a document from the WebDAV server"""
        form = await request.form()
        doc_id = form.get('doc_id')
        
        if not doc_id:
            return RedirectResponse('/', status_code=303)
        
        try:
            logger.info(f"Deleting document with ID: {doc_id}")
            success = document_service.delete_document(doc_id)
            
            if success:
                logger.info(f"Successfully deleted document {doc_id}")
            else:
                logger.warning(f"Failed to delete document {doc_id}")
                
            return RedirectResponse('/', status_code=303)
            
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return Titled("Delete Error", Div(f"Error: {str(e)}", cls="container error"))