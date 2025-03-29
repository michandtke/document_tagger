from fasthtml.common import *
from ui.components.common.navigation import create_navigation
from ui.scripts.metadata.file_preview import get_file_preview_js
from ui.scripts.metadata.metadata_handler import get_metadata_handler_js

def create_metadata_form(filename):
    """
    Create a form for adding metadata to a raw file
    
    Args:
        filename (str): The filename to add metadata to
        
    Returns:
        Div: Metadata form container
    """
    # Create navigation links
    navigation = create_navigation([("Back to Raw Files", "/raw_files")])
    
    metadata_form = Div(
        # Navigation links
        navigation,
        
        Div(
            H2(f"Add Metadata for: {filename}"),
            
            # File preview section
            Div(
                H3("File Preview"),
                Div(id="file-preview-container", cls="file-preview-container"),
                id="file-preview-section",
                cls="file-preview-section"
            ),
            
            # Extracted text preview
            Div(id="extracted-text-preview", cls="extracted-text-preview"),
            
            # Tag suggestions
            Div(
                H3("Tag Suggestions"),
                Div(id="tag-suggestions-container", style="display: flex; flex-wrap: wrap; gap: 8px;"),
                id="tag-suggestions-panel", 
                cls="tag-suggestions-panel"
            ),
            
            # Metadata form
            Form(
                Div(
                    H3("Enter Tags"),
                    Input(type="text", id="tags-input", name="tags", 
                        placeholder="Enter tags separated by commas"),
                    Hidden(id="filename-input", name="filename", value=filename),
                    Div(id="tag-suggestion-notice", cls="tag-suggestion hidden"),
                    cls="form-group"
                ),
                Div(
                    Button("Save Metadata", cls="save-metadata-btn", type="submit"),
                    A("Cancel", href="/raw_files", cls="cancel-btn"),
                    cls="form-buttons"
                ),
                method="POST",
                action="/add_metadata"
            ),
            
            cls="container metadata-page-form"
        ),
        
        # Include all necessary JavaScript explicitly
        Script("""
        // Function to display tag suggestions - copied here for completeness
        function displayTagSuggestions(suggestions) {
            const container = document.getElementById('tag-suggestions-container');
            
            if (!container) return;
            
            // Clear any existing suggestions
            container.innerHTML = '';
            
            // No suggestions
            if (suggestions.length === 0) {
                container.innerHTML = '<div class="no-suggestions">No tag suggestions available</div>';
                return;
            }
            
            // Create a clickable tag suggestion for each suggestion
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
        }

        document.addEventListener('DOMContentLoaded', function() {
            const filename = document.getElementById('filename-input').value;
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
        });
        """),
        Script(get_file_preview_js()),
        Script(get_metadata_handler_js())
    )
    
    return metadata_form