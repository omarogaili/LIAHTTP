from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import time

HOST = '192.168.31.10'
PORT = 3333

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(self.prepare_data())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(f"Received POST request with data: {post_data.decode()}")
        self.send_response(200)
        self.end_headers()

    def prepare_data(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        zone = random.randint(1, 3)
        data = f"ID: {random.randint(1000, 9999)}, Time: {current_time}, Zone: {zone}"
        return bytes(data, 'utf-8')

server = HTTPServer((HOST, PORT), Server)
print(f"Server now running at {HOST}:{PORT}")
server.serve_forever()
