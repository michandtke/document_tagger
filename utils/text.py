import re
import unicodedata

def normalize_text(text):
    """
    Normalize text by removing excess whitespace, normalizing unicode, etc.
    
    Args:
        text (str): Input text
        
    Returns:
        str: Normalized text
    """
    if not text:
        return ""
    
    # Normalize unicode
    text = unicodedata.normalize('NFKD', text)
    
    # Replace multiple whitespace with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    return text.strip()

def normalize_tags(tags_str):
    """
    Normalize a string of comma-separated tags
    
    Args:
        tags_str (str): Comma-separated tags
        
    Returns:
        str: Normalized comma-separated tags
    """
    if not tags_str:
        return ""
        
    # Split by comma, trim whitespace, and remove empty tags
    tags = [tag.strip() for tag in tags_str.split(',')]
    tags = [tag for tag in tags if tag]
    
    # Sort tags for consistency
    tags.sort()
    
    # Join back with commas
    return ', '.join(tags)

def count_tokens(text):
    """
    Estimate the number of tokens in text (rough approximation)
    
    Args:
        text (str): Input text
        
    Returns:
        int: Estimated token count
    """
    if not text:
        return 0
    
    # Simple approximation - word count + punctuation
    return len(re.findall(r'\b\w+\b|[^\w\s]', text))

def truncate_text(text, max_length=100, suffix='...'):
    """
    Truncate text to a maximum length
    
    Args:
        text (str): Input text
        max_length (int): Maximum length
        suffix (str): Suffix to add when truncated
        
    Returns:
        str: Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length].rsplit(' ', 1)[0] + suffix

def extract_keywords(text, max_keywords=10):
    """
    Extract potential keywords from text (simple implementation)
    
    Args:
        text (str): Input text
        max_keywords (int): Maximum number of keywords to extract
        
    Returns:
        list: Extracted keywords
    """
    if not text:
        return []
    
    # Normalize text
    normalized = normalize_text(text.lower())
    
    # Remove common stop words (simplified example)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'of', 'from'}
    
    # Split into words and filter stop words
    words = [word for word in re.findall(r'\b\w{3,}\b', normalized) if word not in stop_words]
    
    # Count word frequencies
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # Get most frequent words
    keywords = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:max_keywords]
    
    return [word for word, count in keywords]