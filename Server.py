from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import time

HOST = '192.168.31.20'
PORT = 3333

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', "application/json")
        self.end_headers()
        self.wfile.write(b'Server is running!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        if post_data.decode()== 'motion':
            print(f"Received POST request with data: {post_data.decode()}")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(self.prepare_data())
        else:
            print(f"Received POST request with data: {post_data.decode()}")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'No motion')

    def prepare_data(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        data = f"ID: {random.randint(1000, 9999)}, Time: {current_time}"
        return bytes(data, 'utf-8')

def start_server():
    server = HTTPServer((HOST, PORT), Server)
    print(f"Server now running at {HOST}:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    start_server()
