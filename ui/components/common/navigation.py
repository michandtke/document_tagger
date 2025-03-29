from fasthtml.common import *

def create_navigation(links):
    """
    Create a navigation bar with links
    
    Args:
        links: List of (text, href) tuples for links
        
    Returns:
        Div: Navigation container
    """
    nav_links = []
    
    for text, href in links:
        nav_links.append(A(text, href=href, cls="nav-link"))
        
    # Add space between links
    for i in range(1, len(nav_links)):
        nav_links.insert(2*i - 1, " ")
        
    return Div(*nav_links, cls="container nav-container")