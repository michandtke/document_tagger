class Styles:
    @staticmethod
    def get_app_css():
        return """
:root {
  --primary-color: #8574c5;
  --secondary-color: #d3cbef;
  --light-color: #f2eeff;
  --table-header-bg: var(--primary-color);
  --table-odd-row-bg: var(--light-color);
  --table-even-row-bg: #ffffff;
  --button-bg: #b8b8b8;
  --success-color: #28a745;
  --error-color: #dc3545;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

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

.new-file-section {
  background-color: var(--secondary-color);
  padding: 15px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.doc-table {
  width: 100%;
  border-collapse: collapse;
}

.doc-table th {
  background-color: var(--table-header-bg);
  color: white;
  text-align: left;
  padding: 12px;
}

.doc-table tr:nth-child(odd) {
  background-color: var(--table-odd-row-bg);
}

.doc-table tr:nth-child(even) {
  background-color: var(--table-even-row-bg);
}

.doc-table td {
  padding: 12px;
}

.delete-btn {
  background-color: #ff5252;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 3px 8px;
  cursor: pointer;
  font-size: 0.85em;
}

.tag {
  background-color: var(--primary-color);
  color: white;
  padding: 3px 8px;
  border-radius: 12px;
  margin-right: 5px;
  display: inline-block;
  font-size: 0.9em;
}

input[type="text"] {
  padding: 8px;
  width: 100%;
  box-sizing: border-box;
}

.hidden {
  display: none;
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

#tags-input {
  width: calc(100% - 70px);
  display: inline-block;
}

.import-result {
  padding: 15px;
  margin: 20px 0;
  border-radius: 4px;
}

.import-result.success {
  background-color: #d4edda;
  color: #155724;
}

.import-result.error {
  background-color: #f8d7da;
  color: #721c24;
}

.loading {
  padding: 10px;
  background-color: #e3f2fd;
  border-radius: 4px;
  text-align: center;
  margin: 10px 0;
}

.error {
  padding: 10px;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 4px;
  text-align: center;
  margin: 10px 0;
}

#similarity-preview {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
  background-color: #f5f5f5;
}

.add-tag-btn:disabled {
  background-color: #9e9e9e;
  cursor: not-allowed;
}

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

.hidden {
  display: none;
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

.tag-suggestions-panel {
  margin-top: 15px;
  padding: 12px;
  background-color: #f5f5f5;
  border-radius: 4px;
  border-left: 3px solid var(--primary-color);
}

.tag-suggestion-button {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  font-size: 0.9em;
}

.tag-suggestion-button:hover {
  border-color: var(--primary-color);
  background-color: #f0f0ff;
}

.tag-suggestion-button.selected {
  border-color: var(--primary-color);
  background-color: #e6e6ff;
  box-shadow: 0 0 0 2px rgba(133, 116, 197, 0.3);
}

.similarity-badge {
  background-color: var(--primary-color);
  color: white;
  border-radius: 12px;
  padding: 2px 6px;
  font-size: 0.8em;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.tag-suggestion-button.selected .similarity-badge {
  animation: pulse 2s infinite;
}

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

/* Highlight row if similarity is high */
.doc-table tr.high-similarity {
  background-color: rgba(133, 116, 197, 0.1);
}

/* Additional style for search result highlighting */
.highlight-match {
  background-color: rgba(255, 235, 59, 0.3);
  padding: 2px 4px;
  border-radius: 3px;
}

/* Add to styles.py */

.raw-files-table {
  width: 100%;
}

.metadata-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
}

.metadata-form {
  margin-top: 20px;
  padding: 20px;
  background-color: var(--light-color);
  border-radius: 6px;
  border-left: 3px solid var(--primary-color);
}

.save-metadata-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  margin-top: 10px;
}

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

.nav-container {
  margin: 20px auto;
  text-align: right;
}

.nav-link {
  display: inline-block;
  padding: 8px 16px;
  background-color: var(--primary-color);
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.text-preview h4 {
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 1em;
  color: #555;
}
"""