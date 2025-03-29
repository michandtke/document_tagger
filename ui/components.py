from fasthtml.common import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UIComponents:
    @staticmethod
    def format_tags(tags_str):
        """
        Format tags for display
        
        Args:
            tags_str: Either a comma-separated string of tags or a list of tags
            
        Returns:
            Div: Formatted tags container
        """
        # Handle both string and list inputs
        if isinstance(tags_str, list):
            tags = tags_str
        else:
            # Split string by comma and strip whitespace
            tags = [tag.strip() for tag in tags_str.split(',')]
        
        # Create tag elements
        return Div(*[Span(tag, cls="tag") for tag in tags])
    
    @staticmethod
    def create_new_file_section():
        return Div(
            Div("New file name", style="flex: 1;"),
            Div(
                Input(type="text", id="tags-input", value="Document, Invoice, New Tag 1", 
                    placeholder="Enter tags separated by commas"),
                Button("Add", cls="add-tag-btn", 
                    onclick="submitNewDocument()"),
                Div(id="tag-suggestion-notice", cls="tag-suggestion hidden"),
                Div(
                    H4("Tag suggestions:", style="margin-bottom: 8px;"),
                    Div(id="tag-suggestions-container", style="display: flex; flex-wrap: wrap; gap: 8px;"),
                    id="tag-suggestions-panel", 
                    cls="tag-suggestions-panel hidden"
                ),
                style="flex: 2;"
            ),
            Div(id="file-type-indicator", style="margin-top: 10px;"),
            Div(id="file-preview", cls="hidden"),
            id="new-file-section", 
            cls="new-file-section hidden",
        )
    
    @staticmethod
    def create_similarity_table(similarities):
        """Create a table showing similarity with other documents"""
        # Create table header
        table_header = Tr(
            Th("Filename", style="width: 70%;"),
            Th("Similarity", style="width: 30%;")
        )
        
        # Create table rows
        table_rows = []
        for doc in similarities[:10]:  # Show top 10 similar documents
            similarity_value = doc['similarity']
            # Calculate color - from light blue (low) to dark blue (high)
            blue_value = max(0, 255 - int(similarity_value * 2))
            color_style = f"background-color: rgb({blue_value}, {blue_value}, 255); color: {'white' if similarity_value > 30 else 'black'};"
            
            table_rows.append(
                Tr(
                    Td(A(doc['filename'], href=f"/?query={doc['filename']}")),
                    Td(f"{similarity_value}%", style=color_style)
                )
            )
        
        if not similarities:
            table_rows.append(
                Tr(
                    Td("No similar documents found", colspan="2", style="text-align: center; padding: 20px;")
                )
            )
        
        # Create table
        return Div(
            Table(
                table_header,
                *table_rows,
                cls="doc-table similarity-table"
            ),
            cls="similarity-container"
        )

    @staticmethod
    def create_document_table(documents, similarities=None):
        """
        Create a table of documents with optional similarity values
        
        Args:
            documents: List of documents
            similarities: Dict of document IDs and their similarity values (optional)
        """
        # Add debug info
        if similarities:
            logger.info(f"Creating table with {len(similarities)} similarity values")
        else:
            logger.info("Creating table without similarity values")
        
        # Create table header
        table_header = Tr(
            Th("Filename", style="width: 25%;"),
            Th("Tags", style="width: 55%;"),
            Th("Simi", style="width: 10%;"),
            Th("", style="width: 10%;")
        )
        
        # Create table rows
        table_rows = []
        for doc in documents:
            doc_id = doc['id']
            
            # Determine similarity value and cell
            similarity_cell = None
            
            # First check the passed similarities dict
            if similarities and doc_id in similarities:
                similarity_value = similarities[doc_id]
                
                # Calculate color - from light blue (low) to dark blue (high)
                blue_value = max(0, 255 - int(similarity_value * 2))
                color_style = f"background-color: rgb({blue_value}, {blue_value}, 255); color: {'white' if similarity_value > 30 else 'black'};"
                
                # Create cell with colored background
                similarity_cell = Td(f"{similarity_value}%", style=color_style)
                
                # Debug
                logger.debug(f"Using similarity from dict for {doc_id}: {similarity_value}%")
                
            # If not in similarities dict, use the document's similarity field
            elif 'similarity' in doc and doc['similarity'] is not None:
                similarity_value = doc['similarity']
                
                # Calculate color - from light blue (low) to dark blue (high)
                blue_value = max(0, 255 - int(similarity_value * 2))
                color_style = f"background-color: rgb({blue_value}, {blue_value}, 255); color: {'white' if similarity_value > 30 else 'black'};"
                
                # Create cell with colored background
                similarity_cell = Td(f"{similarity_value}%", style=color_style)
                
                # Debug
                logger.debug(f"Using similarity from doc for {doc_id}: {similarity_value}%")
                
            # Default case - no similarity information
            else:
                similarity_cell = Td("N/A")
                logger.debug(f"No similarity for {doc_id}")
            
            # Create the table row
            table_rows.append(
                Tr(
                    Td(doc['filename']),
                    Td(UIComponents.format_tags(doc['tags'])),
                    similarity_cell,
                    Td(
                        Form(
                            Button("Delete", cls="delete-btn", type="submit"),
                            Hidden(name="doc_id", value=doc_id),
                            method="POST",
                            action="/delete_document"
                        )
                    )
                )
            )
        
        if not documents:
            table_rows.append(
                Tr(
                    Td("No documents found", colspan="4", style="text-align: center; padding: 20px;")
                )
            )
        
        # Create table
        return Table(
            table_header,
            *table_rows,
            cls="doc-table",
            id="documents-table"
        )
    
    @staticmethod
    def create_search_section(query=None):
        """
        Create a search form section
        
        Args:
            query (str, optional): Pre-filled search query
        
        Returns:
            Div: Search form container
        """
        return Div(
            Form(
                Input(type="text", id="search-input", name="query", 
                    placeholder="Search documents...", value=query or ""),
                Button("Search", type="submit"),
                method="GET",
                action="/search"
            ),
            cls="container search-container"
        )
    
    # ui/components.py (add this method)
    @staticmethod
    def create_raw_files_table(files):
        """
        Create a table of raw files without metadata
        
        Args:
            files: List of file dictionaries
        """
        # Create table header
        table_header = Tr(
            Th("Filename", style="width: 70%;"),
            Th("Actions", style="width: 30%;")
        )
        
        # Create table rows
        table_rows = []
        for file in files:
            table_rows.append(
                Tr(
                    Td(file['filename']),
                    Td(
                        Button("Add Metadata", 
                            cls="metadata-btn",
                            onclick=f"showMetadataForm('{file['filename']}')")
                    )
                )
            )
        
        if not files:
            table_rows.append(
                Tr(
                    Td("No files found", colspan="2", style="text-align: center; padding: 20px;")
                )
            )
        
        # Create metadata form (initially hidden)
        metadata_form = Div(
            H3("Add Metadata"),
            P("Adding metadata for: ", Span("", id="metadata-filename")),
            Div(id="extracted-text-preview", cls="extracted-text-preview"),
            Div(
                H4("Tag suggestions:", style="margin-bottom: 8px;"),
                Div(id="tag-suggestions-container", style="display: flex; flex-wrap: wrap; gap: 8px;"),
                id="tag-suggestions-panel", 
                cls="tag-suggestions-panel hidden"
            ),
            Div(
                Form(
                    Input(type="text", id="tags-input", name="tags", 
                        placeholder="Enter tags separated by commas"),
                    Hidden(id="filename-input", name="filename"),
                    Button("Save Metadata", cls="save-metadata-btn", type="submit"),
                    method="POST",
                    action="/add_metadata"
                ),
                Div(id="tag-suggestion-notice", cls="tag-suggestion hidden")
            ),
            id="metadata-form",
            cls="metadata-form hidden"
        )
        
        # Create table
        return Div(
            Table(
                table_header,
                *table_rows,
                cls="doc-table raw-files-table",
                id="raw-files-table"
            ),
            metadata_form
        )

    @staticmethod
    def create_upload_section(target_folder=None):
        """
        Create file upload section
        
        Args:
            target_folder (str, optional): Target folder for upload
        """
        upload_url = "/upload_document"
        if target_folder:
            upload_url = f"/upload_raw?folder={target_folder}"
            
        return Div(
            Button("Upload new File", cls="upload-btn", 
                onclick="document.getElementById('file-input').click()"),
            Input(type="file", id="file-input", cls="file-input", 
                onchange="handleFileUpload(this)"),
            cls="container"
        )