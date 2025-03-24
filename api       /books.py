from http.server import BaseHTTPRequestHandler
from library_manager import Library, Book
import json

lib = Library()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps([vars(b) for b in lib.books]).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length))
        
        book = Book(
            title=data['title'],
            author=data['author'],
            genre=data['genre'],
            publication_year=int(data['year'])
        )
        lib.add_book(book)
        
        self.send_response(201)
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode())

    def do_DELETE(self):
        title = self.path.split('/')[-1]
        lib.remove_book(title)
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({"status": "deleted"}).encode())
