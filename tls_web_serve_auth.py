from http.server import SimpleHTTPRequestHandler, HTTPServer
import ssl
import base64
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Define your credentials
USERNAME = "username"
PASSWORD = "password"
WEB_ROOT_DIR = '/path/to/transfer'

class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def check_credentials(self, headers):
        auth_header = headers.get('Authorization')
        if not auth_header:
            logging.info("No authorization header received")
            return False
        auth_type, encoded_credentials = auth_header.split(' ', 1)
        if auth_type.lower() != 'basic':
            logging.info("Authorization type is not basic")
            return False
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
        if username == USERNAME and password == PASSWORD:
            return True
        else:
            logging.info("Invalid username or password")
            return False

    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        web_root_path = os.path.join(WEB_ROOT_DIR, relpath)
        logging.info(f"Requested path: {path}, Serving from: {web_root_path}")
        return web_root_path

    def do_GET(self):
        if not self.check_credentials(self.headers):
            self.do_AUTHHEAD()
            self.wfile.write('Unauthorized'.encode())
            return
        super().do_GET()

def run(server_class=HTTPServer, handler_class=AuthHTTPRequestHandler, port=443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    # Create an SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    certfile_path = '/path/to/fullchain.pem'
    keyfile_path = '/path/to/privkey.pem'
    context.load_cert_chain(certfile_path, keyfile_path)

    # Wrap the server socket in the SSL context
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    logging.info(f"Starting HTTPS server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

