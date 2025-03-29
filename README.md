# Document Tagger

A FastHTML-based web application for document management with intelligent tagging and similarity search.

## Features

- **Document Management**: Upload, tag, and organize your documents
- **Smart Tagging**: Get tag suggestions based on document content and similarity to existing documents
- **File Preview**: Preview various file types directly in the browser (images, PDFs, text files)
- **Similarity Search**: Find documents similar to your search query or uploaded files
- **WebDAV Integration**: Store documents in any WebDAV-compatible storage
- **Text Extraction**: Automatically extract text from various document formats
- **Document Cache**: Performance optimized with intelligent caching

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Virtual environment (optional but recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/document_tagger.git
   cd document_tagger
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your WebDAV connection in `config.py` or using environment variables:
   ```python
   # Environment variables
   export WEBDAV_URL="https://your-webdav-server.com"
   export WEBDAV_USERNAME="username"
   export WEBDAV_PASSWORD="password"
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to http://localhost:8000

## Application Structure

```
document_tagger/
├── app.py                # Main application entry point
├── config.py             # Configuration settings
├── models/               # Data models
├── routes/               # Route handlers
│   ├── __init__.py       # Route initialization
│   ├── main.py           # Main document routes
│   ├── search.py         # Search functionality
│   ├── document.py       # Document operations
│   ├── raw_files.py      # Raw file management
│   └── admin.py          # Admin dashboard
├── services/             # Business logic services
│   ├── document_service.py
│   ├── similarity_service.py
│   ├── webdav_service.py
│   ├── text_extraction.py
│   └── document_cache.py
├── ui/                   # UI components
│   ├── components/       # HTML components
│   │   ├── common/       # Shared components
│   │   ├── documents/    # Document list components
│   │   ├── raw_documents/# Raw files components
│   │   └── metadata/     # Metadata editor components
│   ├── styles/           # CSS styles
│   │   ├── common/       # Base styles
│   │   ├── documents/    # Document page styles
│   │   ├── raw_documents/# Raw files styles
│   │   └── metadata/     # Metadata form styles
│   └── scripts/          # JavaScript
│       ├── common/       # Utility scripts
│       ├── documents/    # Document page scripts
│       ├── raw_documents/# Raw files scripts
│       └── metadata/     # Metadata form scripts
└── utils/                # Utility functions
```

## Usage

### Document Management

1. **Upload Documents**:
   - Click "Upload new File" on the home page
   - Select a file from your computer
   - Add tags (the system will suggest tags based on similar documents)
   - Click "Add" to upload

2. **View Documents**:
   - All documents are listed on the home page
   - Documents are displayed with their tags and can be deleted if needed

3. **Search Documents**:
   - Use the search box at the top of the page
   - Results are ranked by relevance (similarity to search query)

### Raw Files Management

1. **View Raw Files**:
   - Click "View Raw Files" in the navigation
   - This shows files that haven't been tagged yet

2. **Add Metadata**:
   - Click "Add Metadata" next to a file
   - The system will analyze the file and suggest tags based on similar documents
   - Add or modify the suggested tags
   - Click "Save Metadata" to move the file to your document library

### Admin Functions

- **Document Cache**: View and manage the document caching system
- **Reload Cache**: Force a reload of the document cache if needed

## Technical Details

### Intelligent Document Tagging

The application uses embedding-based similarity to suggest tags for new documents:

1. When a document is uploaded, its text content is extracted
2. The text is converted to an embedding vector using SentenceTransformers
3. This vector is compared to embeddings of existing documents
4. Tags from the most similar documents are suggested for the new document

### Document Caching

To improve performance, the application includes a document caching system:

1. Documents are loaded once and cached in memory
2. The cache is automatically updated when documents are added or deleted
3. This reduces the number of WebDAV API calls and improves response times

### File Type Support

The application supports a wide range of file types:

- **Images**: JPG, PNG, GIF, etc. (preview available)
- **Documents**: PDF, Word, Excel, PowerPoint (preview for PDFs)
- **Text Files**: TXT, CSV, JSON, XML, etc. (preview available)
- **Other Files**: Any file type can be stored (generic icon shown)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.