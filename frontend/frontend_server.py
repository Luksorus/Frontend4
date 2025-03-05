from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os

PORT = 3000

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/api/products':
            try:
                with open('products.json', 'r', encoding='utf-8') as f:
                    products = json.load(f)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(products).encode('utf-8'))
                return
            except Exception as e:
                self.send_error(500, f'Server error: {str(e)}')
                return
        return super().do_GET()

if __name__ == '__main__':
    server = HTTPServer(('', PORT), RequestHandler)
    print(f"Frontend server running on port {PORT}")
    server.serve_forever()