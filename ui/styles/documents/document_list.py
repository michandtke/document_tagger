def get_document_list_css():
    """
    Get CSS styling for the document list page
    
    Returns:
        str: Document list CSS styling
    """
    return """
/* Upload section */
.upload-btn, .webdav-btn {
  background-color: var(--button-bg);
  color: #000;
  padding: 15px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 20px;
}

.webdav-btn {
  background-color: var(--primary-color);
  color: white;
}

.file-input {
  display: none;
}

/* New file upload section */
.new-file-section {
  background-color: var(--secondary-color);
  padding: 15px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.add-tag-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  margin-left: 8px;
}

.add-tag-btn:disabled {
  background-color: #9e9e9e;
  cursor: not-allowed;
}

#tags-input {
  width: calc(100% - 70px);
  display: inline-block;
}

/* Tag suggestions */
.tag-suggestion {
  font-size: 0.8em;
  color: #4caf50;
  margin-top: 5px;
  padding: 3px 8px;
  background-color: #e8f5e9;
  border-radius: 4px;
  border-left: 3px solid #4caf50;
  animation: fadein 0.5s;
}

@keyframes fadein {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* Search section */
.search-container {
  margin: 20px auto;
}

.search-container form {
  display: flex;
  gap: 10px;
}

.search-container input {
  flex-grow: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-container button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.search-info {
  padding: 10px;
  background-color: var(--light-color);
  border-radius: 4px;
  margin-top: 10px;
  font-style: italic;
}

/* Similarity table styling */
.similarity-container {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
  background-color: #f5f5f5;
}

/* Highlighting for search results */
.highlight-match {
  background-color: rgba(255, 235, 59, 0.3);
  padding: 2px 4px;
  border-radius: 3px;
}

/* Row highlighting for similar documents */
.doc-table tr.high-similarity {
  background-color: rgba(133, 116, 197, 0.1);
}

.calculating {
  opacity: 0.8;
  position: relative;
}

.calculating::after {
  content: "Calculating similarities...";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  z-index: 100;
}
"""