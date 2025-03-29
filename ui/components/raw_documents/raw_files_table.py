from fasthtml.common import *

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
                    A("Add Metadata", 
                        href=f"/add_metadata_form?filename={file['filename']}",
                        cls="metadata-btn")
                )
            )
        )
    
    if not files:
        table_rows.append(
            Tr(
                Td("No files found", colspan="2", style="text-align: center; padding: 20px;")
            )
        )
    
    # Create table
    return Div(
        Table(
            table_header,
            *table_rows,
            cls="doc-table raw-files-table",
            id="raw-files-table"
        )
    )