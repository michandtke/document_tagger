def get_raw_files_css():
    """
    Get CSS styling for the raw files page
    
    Returns:
        str: Raw files CSS styling
    """
    return """
.raw-files-table {
  width: 100%;
}

.metadata-btn {
  background-color: var(--primary-color);
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  text-decoration: none;
  display: inline-block;
  font-size: 0.9em;
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
"""