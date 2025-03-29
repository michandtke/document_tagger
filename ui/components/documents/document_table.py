from fasthtml.common import *
import logging

logger = logging.getLogger(__name__)

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
                Td(format_tags(doc['tags'])),
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