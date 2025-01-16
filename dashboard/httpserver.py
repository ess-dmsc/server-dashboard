import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import argparse
import logging
import htmlsvg
import ssl


class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    logging.basicConfig(level=logging.ERROR)

    def do_GET(self):
        if self.path == '/':
            self.path = './ymir/index.html'
        if self.path == '/dashboard.svg':
            self.path = './ymir/dashboard.svg'
        if self.path == "/logo.jpeg":
            self.path = "./ymir/logo.jpeg"
        if self.path.startswith('/ymir') and self.path.endswith('/ymir'):
            self.path = './ymir/index.html'
        if self.path.startswith('/ess') and self.path.endswith('/ess'):
            self.path = './ess/index.html'
        if self.path.startswith('/utgaard') and self.path.endswith('/utgaard'):
            self.path = './utgaard/index.html'
        else:
            self.path = './' + self.path


        if not os.path.exists(self.path):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(htmlsvg.NOT_SUPPORTED.encode())
            f"<p>Requested path: {self.path}</p>".encode()
            logging.error(f"Failed on equested path: {self.path}")
            return

        return super().do_GET()


def run(server_class=HTTPServer, handler_class=CustomHTTPRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile="/etc/puppetlabs/puppet/ssl/private_keys/dashboard01.novalocal.pem",
        certfile="/etc/puppetlabs/puppet/ssl/certs/dashboard01.novalocal.pem", server_side=True)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8766, help="Port number")
    args = parser.parse_args()

    run(port=args.port)
