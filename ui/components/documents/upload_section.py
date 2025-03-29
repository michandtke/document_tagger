from fasthtml.common import *

def create_upload_section(target_folder=None):
    """
    Create file upload section for documents
    
    Args:
        target_folder (str, optional): Target folder for upload
    """
    upload_url = "/upload_document"
    if target_folder:
        upload_url = f"/upload_raw?folder={target_folder}"
        
    return Div(
        Button("Upload new File", cls="upload-btn", 
            onclick="document.getElementById('file-input').click()"),
        Input(type="file", id="file-input", cls="file-input", 
            onchange="handleFileUpload(this)"),
        cls="container"
    )

def create_new_file_section():
    """Create the section that appears after a file is selected for upload"""
    return Div(
        Div("New file name", style="flex: 1;"),
        Div(
            Input(type="text", id="tags-input", value="Document, Invoice, New Tag 1", 
                placeholder="Enter tags separated by commas"),
            Button("Add", cls="add-tag-btn", 
                onclick="submitNewDocument()"),
            Div(id="tag-suggestion-notice", cls="tag-suggestion hidden"),
            Div(
                H4("Tag suggestions:", style="margin-bottom: 8px;"),
                Div(id="tag-suggestions-container", style="display: flex; flex-wrap: wrap; gap: 8px;"),
                id="tag-suggestions-panel", 
                cls="tag-suggestions-panel hidden"
            ),
            style="flex: 2;"
        ),
        Div(id="file-type-indicator", style="margin-top: 10px;"),
        Div(id="file-preview", cls="hidden"),
        id="new-file-section", 
        cls="new-file-section hidden",
    )