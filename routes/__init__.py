from fasthtml.common import *
from services.document_service import DocumentService
from services.similarity_service import SimilarityService
from ui.components import UIComponents
from ui.styles import Styles
from ui.scripts import Scripts

# Initialize services once
document_service = None
similarity_service = None

def init_services(app):
    """Initialize services for routes"""
    global document_service, similarity_service
    
    from config import webdav_config, embedding_config
    from services.webdav_service import WebDAVService
    
    # Initialize services
    webdav_service = WebDAVService(
        webdav_url=webdav_config['url'],
        webdav_username=webdav_config['username'],
        webdav_password=webdav_config['password'],
        folder_path=webdav_config['folder'],
        folder_path_raw=webdav_config['raw_folder']
    )
    
    document_service = DocumentService(webdav_service)
    
    similarity_service = SimilarityService(
        document_service=document_service,
        model_name=embedding_config['model']
    )
    
    # Register routes
    from routes.main import register_routes as register_main_routes
    from routes.search import register_routes as register_search_routes
    from routes.document import register_routes as register_document_routes
    from routes.raw_files import register_routes as register_raw_files_routes
    
    register_main_routes(app)
    register_search_routes(app)
    register_document_routes(app)
    register_raw_files_routes(app)
    