from http.server import SimpleHTTPRequestHandler, HTTPServer
import ssl
import base64
import os

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
            return False
        auth_type, encoded_credentials = auth_header.split(' ', 1)
        if auth_type.lower() != 'basic':
            return False
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
        return username == USERNAME and password == PASSWORD

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored. (XXX They should
        probably be diagnosed.)
        """
        # Ensure the path is within the web root directory
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        return os.path.join(WEB_ROOT_DIR, relpath)

    def do_GET(self):
        if not self.check_credentials(self.headers):
            self.do_AUTHHEAD()
            self.wfile.write('Unauthorized'.encode())
            return
        super().do_GET()

def run(server_class=HTTPServer, handler_class=AuthHTTPRequestHandler, port=443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    # Specify the path to your certificate and key
    certfile_path = '/path/to/fullchain.pem'
    keyfile_path = '/path/to/privkey.pem'

    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certfile_path, keyfile=keyfile_path, server_side=True)
    print(f"Starting HTTPS server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

