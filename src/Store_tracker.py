from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random
import json



HOST = '192.168.31.24'
PORT = 3333

class Store_tracker (BaseHTTPRequestHandler):
    """
    This class simulates the Store Tracker App. It receives mocked customer flow data from the sesame sensor.
    """
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', "application/json")
        self.end_headers()
        self.wfile.write(b'Store tracker is running!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        data = json.loads(post_data)
        if data.get('message') == 'no motion':
            print(f"Received POST request with data: {post_data}")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"response": "no motion"}).encode())
        else:
            print(f"Received POST request with data: {post_data}")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"response": "OK"}).encode())

def start_server():
    server = HTTPServer((HOST, PORT), Store_tracker )
    print(f"Server now running at {HOST}:{PORT}")
    server.serve_forever()

def shutdown_server():
    server = HTTPServer((HOST, PORT), Store_tracker )
    server.shutdown()
    server.server_close()

if __name__ == "__main__":
    start_server()
