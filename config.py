import os

# config.py
webdav_config = {
    'url': os.getenv('WEBDAV_URL', 'https://webdav.example.com'),
    'username': os.getenv('WEBDAV_USERNAME', ''),
    'password': os.getenv('WEBDAV_PASSWORD', ''),
    'folder': '/documents',
    'raw_folder': '/raw_documents'
}

embedding_config = {
    'model': 'all-MiniLM-L6-v2',
    'similarity_threshold': 30,
    'max_suggestions': 3
}

log_config = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}