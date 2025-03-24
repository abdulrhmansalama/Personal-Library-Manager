import csv
import os
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Book:
    """Represents a book in the library"""
    title: str
    author: str
    genre: str
    publication_year: int

class Library:
    """Manages a collection of books with CRUD operations and file persistence"""
    
    def __init__(self, file_path: str = "library.csv"):
        self.file_path = file_path
        self.books: List[Book] = []
        self.load_library()
    
    def add_book(self, book: Book) -> None:
        """Add a book to the library"""
        self.books.append(book)
        self.save_library()
        print(f"Book '{book.title}' added successfully!")
    
    def remove_book(self, title: str) -> None:
        """Remove a book by title"""
        initial_count = len(self.books)
        self.books = [book for book in self.books if book.title.lower() != title.lower()]
        
        if len(self.books) < initial_count:
            self.save_library()
            print(f"Book '{title}' removed successfully!")
        else:
            print(f"Book '{title}' not found in the library.")
    
    def search_by_title(self, title: str) -> List[Book]:
        """Search for books by title (case-insensitive partial match)"""
        return [book for book in self.books if title.lower() in book.title.lower()]
    
    def search_by_author(self, author: str) -> List[Book]:
        """Search for books by author (case-insensitive partial match)"""
        return [book for book in self.books if author.lower() in book.author.lower()]
    
    def display_all(self) -> None:
        """Display all books in the library"""
        if not self.books:
            print("The library is empty.")
            return
        
        print("\n=== Library Contents ===")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book.title} by {book.author} ({book.publication_year}) - {book.genre}")
        print("=======================\n")
    
    def save_library(self) -> None:
        """Save the library data to a CSV file"""
        try:
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['title', 'author', 'genre', 'publication_year'])
                for book in self.books:
                    writer.writerow([book.title, book.author, book.genre, book.publication_year])
        except IOError as e:
            print(f"Error saving library: {e}")
    
    def load_library(self) -> None:
        """Load the library data from a CSV file"""
        if not os.path.exists(self.file_path):
            return
            
        try:
            with open(self.file_path, 'r') as file:
                reader = csv.DictReader(file)
                self.books = [
                    Book(
                        title=row['title'],
                        author=row['author'],
                        genre=row['genre'],
                        publication_year=int(row['publication_year'])
                    ) for row in reader
                ]
        except (IOError, ValueError, KeyError) as e:
            print(f"Error loading library: {e}")
            self.books = []

def get_user_input(prompt: str, validator=None) -> str:
    """Helper function to get validated user input"""
    while True:
        try:
            user_input = input(prompt).strip()
            if validator and not validator(user_input):
                raise ValueError("Invalid input")
            return user_input
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def main_menu() -> None:
    """Main interactive menu for the library system"""
    library = Library()
    
    while True:
        print("\n=== Personal Library Management System ===")
        print("1. Add a new book")
        print("2. Remove a book")
        print("3. Search for a book by title")
        print("4. Search for a book by author")
        print("5. Display all books")
        print("6. Exit")
        
        choice = get_user_input("Enter your choice (1-6): ", lambda x: x in ['1', '2', '3', '4', '5', '6'])
        
        if choice == '1':
            print("\nAdd a new book:")
            title = get_user_input("Title: ", lambda x: len(x) > 0)
            author = get_user_input("Author: ", lambda x: len(x) > 0)
            genre = get_user_input("Genre: ", lambda x: len(x) > 0)
            year = get_user_input("Publication Year: ", lambda x: x.isdigit() and int(x) > 0)
            
            book = Book(title=title, author=author, genre=genre, publication_year=int(year))
            library.add_book(book)
            
        elif choice == '2':
            title = get_user_input("Enter the title of the book to remove: ")
            library.remove_book(title)
            
        elif choice == '3':
            title = get_user_input("Enter the title to search: ")
            results = library.search_by_title(title)
            display_search_results(results)
            
        elif choice == '4':
            author = get_user_input("Enter the author to search: ")
            results = library.search_by_author(author)
            display_search_results(results)
            
        elif choice == '5':
            library.display_all()
            
        elif choice == '6':
            print("Thank you for using the Personal Library Management System. Goodbye!")
            break

def display_search_results(results: List[Book]) -> None:
    """Display search results to the user"""
    if not results:
        print("No matching books found.")
    else:
        print("\n=== Search Results ===")
        for i, book in enumerate(results, 1):
            print(f"{i}. {book.title} by {book.author} ({book.publication_year}) - {book.genre}")
        print("=====================\n")

if __name__ == "__main__":
    main_menu()