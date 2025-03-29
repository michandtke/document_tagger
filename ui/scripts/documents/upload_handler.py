def get_upload_handler_js():
    """
    Get JavaScript for handling document uploads
    
    Returns:
        str: Document upload handler JavaScript
    """
    return """
let currentFileName = '';

async function handleFileUpload(input) {
    if (input.files && input.files[0]) {
        currentFileName = input.files[0].name;
        // Show the new file section
        const newFileSection = document.getElementById('new-file-section');
        newFileSection.classList.remove('hidden');
        
        // Update the new file section with the file name
        newFileSection.children[0].textContent = currentFileName;
        
        // Create file preview if possible
        const fileType = input.files[0].type;
        if (fileType.startsWith('image/')) {
            createImagePreview(input.files[0]);
        } else if (fileType === 'application/pdf') {
            document.getElementById('file-type-indicator').textContent = 'PDF Document';
        } else if (fileType.includes('word')) {
            document.getElementById('file-type-indicator').textContent = 'Word Document';
        } else if (fileType.includes('excel') || fileType.includes('spreadsheet')) {
            document.getElementById('file-type-indicator').textContent = 'Spreadsheet';
        } else {
            document.getElementById('file-type-indicator').textContent = fileType || 'Unknown file type';
        }
        
        // Get similarity for existing documents
        await getPreviewSimilarity(input.files[0]);
    }
}

function createImagePreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewContainer = document.getElementById('file-preview');
        if (previewContainer) {
            previewContainer.innerHTML = `<img src="${e.target.result}" style="max-width: 100%; max-height: 200px;" />`;
            previewContainer.classList.remove('hidden');
        }
    }
    reader.readAsDataURL(file);
}

async function getPreviewSimilarity(file) {
    try {
        // Get tags from input
        const tagsInput = document.getElementById('tags-input');
        const tags = tagsInput.value.trim();
        
        // Create a FormData to send file
        const formData = new FormData();
        formData.append('file', file);
        formData.append('tags', tags);
        
        // Show loading indicator
        const similarityContainer = document.getElementById('similarity-preview');
        if (similarityContainer) {
            similarityContainer.innerHTML = '<div class="loading">Calculating similarities...</div>';
            similarityContainer.classList.remove('hidden');
        }
        
        // Send to endpoint for similarity calculation
        const response = await fetch('/preview_similarity', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            
            // Show tag suggestion panel if suggestions exist
            if (result.tag_suggestions && result.tag_suggestions.length > 0) {
                displayTagSuggestions(result.tag_suggestions);
                
                // Show the suggestions panel
                const panel = document.getElementById('tag-suggestions-panel');
                if (panel) {
                    panel.classList.remove('hidden');
                }
            }
            
            // Update tags input if suggestions exist
            if (result.suggested_tags && tagsInput) {
                const currentTags = tagsInput.value.trim();
                // Only update if user hasn't already entered custom tags
                if (!currentTags || currentTags === "Document, Invoice, New Tag 1") {
                    tagsInput.value = result.suggested_tags;
                    
                    // Show a notification that tags were suggested
                    const tagNotification = document.getElementById('tag-suggestion-notice');
                    if (tagNotification) {
                        tagNotification.textContent = 'Tags suggested from similar document';
                        tagNotification.classList.remove('hidden');
                        
                        // Hide the notification after 5 seconds
                        setTimeout(() => {
                            tagNotification.classList.add('hidden');
                        }, 5000);
                    }
                }
            }
        } else {
            console.error('Failed to get similarities');
            if (similarityContainer) {
                similarityContainer.innerHTML = '<div class="error">Failed to calculate similarities</div>';
            }
        }
    } catch (error) {
        console.error('Error getting similarities:', error);
        const similarityContainer = document.getElementById('similarity-preview');
        if (similarityContainer) {
            similarityContainer.innerHTML = '<div class="error">Error: ' + error.message + '</div>';
        }
    }
}

function submitNewDocument() {
    if (!currentFileName) return;
    
    const tagsInput = document.getElementById('tags-input');
    const tags = tagsInput.value.trim();
    
    if (!tags) {
        alert('Please enter at least one tag');
        return;
    }
    
    // Get the actual file
    const fileInput = document.getElementById('file-input');
    if (!fileInput.files || !fileInput.files[0]) {
        alert('Please select a file');
        return;
    }
    
    // Create a FormData object to properly handle the file upload
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('tags', tags);
    
    // Show upload indicator
    const uploadButton = document.querySelector('.add-tag-btn');
    if (uploadButton) {
        uploadButton.textContent = 'Uploading...';
        uploadButton.disabled = true;
    }
    
    // Use fetch API to upload
    fetch('/upload_document', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            window.location.href = '/';
        } else {
            console.error('Upload failed');
            alert('Upload failed');
            if (uploadButton) {
                uploadButton.textContent = 'Add';
                uploadButton.disabled = false;
            }
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('Error: ' + error);
        if (uploadButton) {
            uploadButton.textContent = 'Add';
            uploadButton.disabled = false;
        }
    });
}
"""