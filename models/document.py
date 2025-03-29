# models/document.py
class Document:
    """Document data model"""
    
    def __init__(self, id, filename, tags, embedding=None, similarity=None):
        self.id = id
        self.filename = filename
        self.tags = tags
        self.embedding = embedding or []
        self.similarity = similarity
    
    @classmethod
    def from_dict(cls, data):
        """Create Document from dictionary"""
        return cls(
            id=data.get('id'),
            filename=data.get('filename'),
            tags=data.get('tags', ''),
            embedding=data.get('embedding', []),
            similarity=data.get('similarity')
        )
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'tags': self.tags,
            'embedding': self.embedding,
            'similarity': self.similarity
        }