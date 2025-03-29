from fasthtml.common import *

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