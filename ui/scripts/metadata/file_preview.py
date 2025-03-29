def get_file_preview_js():
    """
    Get JavaScript for handling file previews
    
    Returns:
        str: File preview handler JavaScript
    """
    return """
// Function to load file preview based on file type
async function loadFilePreview(filename, container) {
    try {
        // Get the file extension
        const ext = filename.split('.').pop().toLowerCase();
        
        // Create a URL to stream the file content
        const previewUrl = '/raw_file_preview?filename=' + encodeURIComponent(filename);
        
        // Display preview based on file type
        if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'].includes(ext)) {
            // Image preview
            container.innerHTML = `<img src="${previewUrl}" alt="${filename}" />`;
        } 
        else if (ext === 'pdf') {
            // PDF preview using iframe
            container.innerHTML = `<iframe class="pdf-preview" src="${previewUrl}" title="${filename}"></iframe>`;
        }
        else if (['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'].includes(ext)) {
            // Office document icon
            const docType = {
                'doc': 'Word', 'docx': 'Word',
                'xls': 'Excel', 'xlsx': 'Excel',
                'ppt': 'PowerPoint', 'pptx': 'PowerPoint'
            }[ext];
            
            container.innerHTML = `
                <div class="unsupported-file">
                    <div class="document-icon">📄</div>
                    <div>${docType} Document</div>
                    <div class="file-info">${filename}</div>
                </div>
            `;
        }
        else if (['txt', 'csv', 'json', 'xml', 'html', 'css', 'js'].includes(ext)) {
            // Try to fetch and display text content
            try {
                const response = await fetch(previewUrl);
                if (response.ok) {
                    const text = await response.text();
                    container.innerHTML = `<pre style="white-space: pre-wrap; max-height: 300px; overflow: auto;">${text.substring(0, 5000)}</pre>`;
                    if (text.length > 5000) {
                        container.innerHTML += '<div class="file-info">(Preview truncated, showing first 5000 characters)</div>';
                    }
                } else {
                    throw new Error('Failed to load text content');
                }
            } catch (e) {
                container.innerHTML = `
                    <div class="unsupported-file">
                        <div class="document-icon">📄</div>
                        <div>Text Document</div>
                        <div class="file-info">${filename}</div>
                    </div>
                `;
            }
        }
        else {
            // Generic file icon for unsupported types
            container.innerHTML = `
                <div class="unsupported-file">
                    <div class="document-icon">📄</div>
                    <div>File Preview Not Available</div>
                    <div class="file-info">${filename}</div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading file preview:', error);
        container.innerHTML = `
            <div class="unsupported-file">
                <div class="document-icon">❌</div>
                <div>Error Loading Preview</div>
                <div class="file-info">${error.message}</div>
            </div>
        `;
    }
}
"""