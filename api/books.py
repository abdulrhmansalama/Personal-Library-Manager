from http.server import BaseHTTPRequestHandler
from lib.library import Library
from lib.book import Book
import json

def handle_request(handler):
    lib = Library()
    
    if handler.command == 'GET':
        handler.send_response(200)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps(lib.books).encode())
    
    elif handler.command == 'POST':
        content_length = int(handler.headers['Content-Length'])
        post_data = json.loads(handler.rfile.read(content_length))
        
        new_book = Book(**post_data)
        lib.add_book(new_book)
        
        handler.send_response(201)
        handler.end_headers()
        handler.wfile.write(json.dumps({'status': 'success'}).encode())

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        handle_request(self)
    
    def do_POST(self):
        handle_request(self)

def app(request):
    handler = Handler(request)
    handler.handle()
    return handler
