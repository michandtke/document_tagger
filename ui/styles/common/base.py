def get_base_css():
    """
    Get base CSS styling used across all pages
    
    Returns:
        str: Base CSS styling
    """
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

/* Navigation */
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

/* Utility classes */
.hidden {
  display: none;
}

/* Messages and notifications */
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

/* Tables base */
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

/* Form elements common */
input[type="text"] {
  padding: 8px;
  width: 100%;
  box-sizing: border-box;
}

/* Tags styling */
.tag {
  background-color: var(--primary-color);
  color: white;
  padding: 3px 8px;
  border-radius: 12px;
  margin-right: 5px;
  display: inline-block;
  font-size: 0.9em;
}

/* Buttons */
.delete-btn {
  background-color: #ff5252;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 3px 8px;
  cursor: pointer;
  font-size: 0.85em;
}

"""