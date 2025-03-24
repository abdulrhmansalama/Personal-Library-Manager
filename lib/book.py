from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    genre: str
    publication_year: int
    
    def to_dict(self):
        """تحويل الكائن لقاموس"""
        return {
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'publication_year': self.publication_year
        }
