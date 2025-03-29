def get_metadata_handler_js():
    """
    Get JavaScript for handling metadata operations
    
    Returns:
        str: Metadata handler JavaScript
    """
    return """
// Function to get file similarities and tag suggestions
async function getFileSimilarities(filename) {
    try {
        // Create form data
        const formData = new FormData();
        formData.append('filename', filename);
        
        // Send to endpoint for similarity calculation
        const response = await fetch('/preview_raw_similarity', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            
            // Update extracted text preview
            const extractedTextPreview = document.getElementById('extracted-text-preview');
            if (extractedTextPreview) {
                if (result.extracted_text_sample) {
                    extractedTextPreview.innerHTML = `<div class="text-preview">
                        <h4>Extracted Content (sample):</h4>
                        <pre>${result.extracted_text_sample}</pre>
                    </div>`;
                } else {
                    extractedTextPreview.innerHTML = '';
                }
            }
            
            // Auto-fill tags if suggested tags are available
            const tagsInput = document.getElementById('tags-input');
            if (tagsInput && result.suggested_tags) {
                tagsInput.value = result.suggested_tags;
                
                // Show notification about auto-filled tags
                const notification = document.getElementById('tag-suggestion-notice');
                if (notification) {
                    notification.textContent = 'Tags automatically suggested based on similar document';
                    notification.classList.remove('hidden');
                    
                    // Hide after 5 seconds
                    setTimeout(() => {
                        notification.classList.add('hidden');
                    }, 5000);
                }
            }
            
            // Display tag suggestions
            if (result.tag_suggestions && result.tag_suggestions.length > 0) {
                displayTagSuggestions(result.tag_suggestions);
            }
        } else {
            console.error('Failed to get similarities');
            const extractedTextPreview = document.getElementById('extracted-text-preview');
            if (extractedTextPreview) {
                extractedTextPreview.innerHTML = '<div class="error">Failed to analyze file</div>';
            }
        }
    } catch (error) {
        console.error('Error getting similarities:', error);
        const extractedTextPreview = document.getElementById('extracted-text-preview');
        if (extractedTextPreview) {
            extractedTextPreview.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    }
}

// Initialize metadata form page
function initMetadataForm() {
    const filename = document.getElementById('filename-input')?.value;
    if (filename) {
        // Display file preview
        const previewContainer = document.getElementById('file-preview-container');
        if (previewContainer) {
            previewContainer.innerHTML = '<div class="loading">Loading file preview...</div>';
            loadFilePreview(filename, previewContainer);
        }
        
        // Show loading indicator for extracted text
        const extractedTextPreview = document.getElementById('extracted-text-preview');
        if (extractedTextPreview) {
            extractedTextPreview.innerHTML = '<div class="loading">Analyzing file content...</div>';
        }
        
        // Get file similarities and tag suggestions
        getFileSimilarities(filename);
    }
}

// Run initialization on DOMContentLoaded
document.addEventListener('DOMContentLoaded', initMetadataForm);
"""