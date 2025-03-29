def get_raw_files_table_js():
    """
    Get JavaScript for handling raw files table operations
    
    Returns:
        str: Raw files table handler JavaScript
    """
    return """
async function updateTableSimilarities(similarities) {
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
"""