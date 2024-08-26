import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import argparse

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = './ymir/index.html'
        if self.path.startswith('/ymir'):
            self.path = './ymir/index.html'
        elif self.path.startswith('/ess'):
            self.path = './ess/index.html'
        elif self.path.startswith('/utgaard'):
            self.path = './utgaard' + self.path[len('/utgaard'):]
        
        if not os.path.exists(self.path):
            self.path = 'not_supported.html'
        
        return super().do_GET()

def run(server_class=HTTPServer, handler_class=CustomHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8766, help='Port number')
    args = parser.parse_args()
    
    run(port=args.port)