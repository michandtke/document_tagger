def get_metadata_form_css():
    """
    Get CSS styling for the metadata form page
    
    Returns:
        str: Metadata form CSS styling
    """
    return """
/* Metadata form page */
.metadata-page-form {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin: 20px auto;
}

.metadata-page-form h2 {
  color: var(--primary-color);
  margin-bottom: 20px;
  border-bottom: 2px solid var(--light-color);
  padding-bottom: 10px;
}

.metadata-page-form h3 {
  color: #333;
  margin: 20px 0 10px 0;
  font-size: 1.2em;
}

.form-group {
  margin-bottom: 20px;
}

.form-group input[type="text"] {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.save-metadata-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
}

.save-metadata-btn:hover {
  background-color: #705bb6;
}

.cancel-btn {
  background-color: #e0e0e0;
  color: #333;
  border: none;
  padding: 12px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  text-decoration: none;
  text-align: center;
  font-weight: 500;
}

.cancel-btn:hover {
  background-color: #d0d0d0;
}

/* File preview section */
.file-preview-section {
  margin: 15px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #ddd;
}

.file-preview-container {
  max-width: 100%;
  overflow: auto;
  margin-top: 10px;
  background-color: white;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #eee;
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-preview-container img {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
}

.file-preview-container .pdf-preview {
  width: 100%;
  height: 400px;
  border: none;
}

.file-preview-container .document-icon {
  font-size: 64px;
  color: var(--primary-color);
  opacity: 0.8;
  margin-bottom: 10px;
}

.file-preview-container .unsupported-file {
  text-align: center;
  color: #666;
}

.file-info {
  margin-top: 10px;
  font-size: 0.9em;
  color: #666;
}

/* Extracted text preview */
.extracted-text-preview {
  margin: 15px 0;
  max-height: 200px;
  overflow-y: auto;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.extracted-text-preview pre {
  white-space: pre-wrap;
  margin: 0;
  font-size: 0.9em;
}

.text-preview h4 {
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 1em;
  color: #555;
}
"""