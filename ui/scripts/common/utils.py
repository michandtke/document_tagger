def get_utils_js():
    """
    Get common utility JavaScript functions
    
    Returns:
        str: Common utility JavaScript
    """
    return """
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

// Function to display tag suggestions
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

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    highlightSearchResults();
});
"""