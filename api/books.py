from http.server import BaseHTTPRequestHandler
import json
from lib.library import Library
from lib.book import Book

def handle_request(handler):
    lib = Library()
    
    if handler.command == 'GET':
        books = [book.to_dict() for book in lib.books]
        handler.send_response(200)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps(books).encode())
    
    elif handler.command == 'POST':
        content_length = int(handler.headers['Content-Length'])
        post_data = json.loads(handler.rfile.read(content_length))
        
        new_book = Book(
            title=post_data['title'],
            author=post_data['author'],
            genre=post_data['genre'],
            publication_year=int(post_data['publication_year'])
        )
        
        lib.add_book(new_book)
        handler.send_response(201)
        handler.end_headers()
        handler.wfile.write(json.dumps({'status': 'success'}).encode())
    
    elif handler.command == 'DELETE':
        title = handler.path.split('/')[-1]
        lib.remove_book(title)
        handler.send_response(200)
        handler.end_headers()
        handler.wfile.write(json.dumps({'status': 'deleted'}).encode())

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        handle_request(self)
    
    def do_POST(self):
        handle_request(self)
    
    def do_DELETE(self):
        handle_request(self)

def app(request):
    handler = Handler(request)
    handler.handle()
    return handler

