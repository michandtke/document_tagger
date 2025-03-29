import os
import tempfile
import mimetypes
from pathlib import Path

def get_file_extension(filename):
    """
    Get the file extension from a filename
    
    Args:
        filename (str): File name
        
    Returns:
        str: File extension (lowercase) or empty string
    """
    return os.path.splitext(filename)[1].lower()

def get_mime_type(filename):
    """
    Get the MIME type for a file
    
    Args:
        filename (str): File name
        
    Returns:
        tuple: (mime_type, encoding)
    """
    return mimetypes.guess_type(filename)

def create_temp_file(content, suffix=None):
    """
    Create a temporary file with given content
    
    Args:
        content (bytes/str): File content
        suffix (str, optional): File extension
        
    Returns:
        str: Path to temporary file
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_path = temp_file.name
        if isinstance(content, str):
            temp_file.write(content.encode('utf-8'))
        else:
            temp_file.write(content)
    
    return temp_path

def ensure_dir_exists(directory):
    """
    Create directory if it doesn't exist
    
    Args:
        directory (str): Directory path
        
    Returns:
        str: Directory path
    """
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def clean_filename(filename):
    """
    Clean a filename to be safe for storage
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Cleaned filename
    """
    # Replace potentially problematic characters
    clean = filename.replace('/', '_').replace('\\', '_')
    
    # Limit length to prevent issues
    if len(clean) > 255:
        ext = get_file_extension(clean)
        clean = clean[:255-len(ext)] + ext
    
    return clean