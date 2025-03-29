class Scripts:
    @staticmethod
    def get_client_js():
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
        await getDocumentSimilarities(input.files[0]);
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
            
            // Update similarity container
            if (similarityContainer) {
                similarityContainer.innerHTML = result.similarity_html;
            }
            
            // Show tag suggestion panel if suggestions exist
            if (result.tag_suggestions && result.tag_suggestions.length > 0) {
                displayTagSuggestions(result.tag_suggestions);
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

// Very basic approach without regex
function highlightSearchResults() {
    // Get search query from URL
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('query');
    
    if (query && query.length > 0) {
        // Get all text nodes in tag spans
        const tags = document.querySelectorAll('.tag');
        
        // Highlight matching tags
        tags.forEach(tag => {
            if (tag.textContent.toLowerCase().includes(query.toLowerCase())) {
                tag.classList.add('highlighted-tag');
            }
        });
        
        // Highlight rows with high similarity
        const rows = document.querySelectorAll('.doc-table tr');
        rows.forEach(row => {
            const similarityCell = row.querySelector('td:nth-child(3)');
            if (similarityCell) {
                const similarityText = similarityCell.textContent;
                const similarityValue = parseInt(similarityText);
                if (similarityValue && similarityValue > 70) { // High similarity threshold
                    row.classList.add('high-similarity');
                }
            }
        });
    }
}

async function getDocumentSimilarities(file) {
    try {
        // Get tags from input
        const tagsInput = document.getElementById('tags-input');
        const tags = tagsInput.value.trim();
        
        // Create a FormData to send file
        const formData = new FormData();
        formData.append('file', file);
        formData.append('tags', tags);
        
        // Show loading indicator
        const tableContainer = document.getElementById('documents-table');
        if (tableContainer) {
            // Add loading class to the table
            tableContainer.classList.add('calculating');
        }
        
        // Send to endpoint for similarity calculation
        const response = await fetch('/preview_similarity', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            
            // Update similarities in the table
            if (result.similarities) {
                updateTableSimilarities(result.similarities);
            }
            
            // Update tag suggestions if available
            if (result.tag_suggestions && result.tag_suggestions.length > 0) {
                displayTagSuggestions(result.tag_suggestions);
            } else {
                // Hide tag suggestions panel if no suggestions
                const suggestionPanel = document.getElementById('tag-suggestions-panel');
                if (suggestionPanel) {
                    suggestionPanel.classList.add('hidden');
                }
            }
        } else {
            console.error('Failed to get similarities');
        }
        
        // Remove loading class
        if (tableContainer) {
            tableContainer.classList.remove('calculating');
        }
    } catch (error) {
        console.error('Error getting similarities:', error);
        
        const tableContainer = document.getElementById('documents-table');
        if (tableContainer) {
            tableContainer.classList.remove('calculating');
        }
    }
}

function displayTagSuggestions(suggestions) {
    const container = document.getElementById('tag-suggestions-container');
    const panel = document.getElementById('tag-suggestions-panel');
    
    if (!container || !panel) return;
    
    // Clear any existing suggestions
    container.innerHTML = '';
    
    // No suggestions
    if (suggestions.length === 0) {
        panel.classList.add('hidden');
        return;
    }
    
    // Create a clickable tag suggestion for each suggestion
    // (server has already filtered for uniqueness)
    suggestions.forEach(suggestion => {
        const button = document.createElement('button');
        button.className = 'tag-suggestion-button';
        button.title = `From ${suggestion.filename} (${suggestion.similarity}% similar)`;
        button.innerHTML = `<span>${suggestion.tags}</span> <span class="similarity-badge">${suggestion.similarity}%</span>`;
        
        // Add click handler to use these tags
        button.addEventListener('click', () => {
            const tagsInput = document.getElementById('tags-input');
            if (tagsInput) {
                tagsInput.value = suggestion.tags;
                
                // Show notification
                const notification = document.getElementById('tag-suggestion-notice');
                if (notification) {
                    notification.textContent = `Tags applied from ${suggestion.filename}`;
                    notification.classList.remove('hidden');
                    
                    // Hide after 5 seconds
                    setTimeout(() => {
                        notification.classList.add('hidden');
                    }, 5000);
                }
                
                // Highlight the used suggestion
                container.querySelectorAll('.tag-suggestion-button').forEach(btn => {
                    btn.classList.remove('selected');
                });
                button.classList.add('selected');
            }
        });
        
        container.appendChild(button);
    });
    
    // Show the panel
    panel.classList.remove('hidden');
}

function updateTableSimilarities(similarities) {
    const table = document.getElementById('documents-table');
    if (!table) return;
    
    // Get all rows except header
    const rows = table.querySelectorAll('tr:not(:first-child)');
    
    rows.forEach(row => {
        // Find the document ID in the hidden input of the delete form
        const hiddenInput = row.querySelector('input[name="doc_id"]');
        if (!hiddenInput) return;
        
        const docId = hiddenInput.value;
        if (docId && similarities[docId] !== undefined) {
            // Get similarity value
            const similarity = similarities[docId];
            
            // Get the similarity cell (3rd column)
            const simiCell = row.cells[2];
            if (!simiCell) return;
            
            // Calculate color - from light blue (low) to dark blue (high)
            const blueValue = Math.max(0, 255 - Math.round(similarity * 2));
            const textColor = similarity > 30 ? 'white' : 'black';
            
            // Update cell
            simiCell.textContent = similarity + '%';
            simiCell.style.backgroundColor = `rgb(${blueValue}, ${blueValue}, 255)`;
            simiCell.style.color = textColor;
        }
    });
}

// Add this function to the client JavaScript

function showMetadataForm(filename) {
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
}

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
            
            // Update similarities in the main document table if it exists
            if (result.similarities) {
                updateTableSimilarities(result.similarities);
            }
            
            // Display tag suggestions
            if (result.tag_suggestions && result.tag_suggestions.length > 0) {
                displayTagSuggestions(result.tag_suggestions);
            } else {
                // Hide tag suggestions panel if no suggestions
                const suggestionPanel = document.getElementById('tag-suggestions-panel');
                if (suggestionPanel) {
                    suggestionPanel.classList.add('hidden');
                }
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

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    highlightSearchResults();
});
"""