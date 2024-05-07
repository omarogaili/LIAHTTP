# from http.server import BaseHTTPRequestHandler, HTTPServer
# import random
# import time

# # HOST = '192.168.31.10'
# HOST = '192.168.1.99'
# PORT = 3333

# class Server(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(self.prepare_data(data))

#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length)
#         print(f"Received POST request with data: {post_data.decode()}")
#         if post_data.decode() == "Motion":
#             self.wfile.write(self.prepare_data(post_data))
#         else:
#             self.wfile.write(b" NO Motion")
#         self.wfile.write(b"No Motion")
#         self.send_response(200)
#         self.end_headers()

#     def prepare_data(self, data):
#         if data == "Motion":
#             current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
#             zone = random.randint(1, 3)
#             data = f"ID: {random.randint(1000, 9999)}, Time: {current_time}, Zone: {zone}"
#             return bytes(data, 'utf-8')
#         else:
#             return b"No Motion"

# server = HTTPServer((HOST, PORT), Server)
# print(f"Server now running at {HOST}:{PORT}")
# server.serve_forever()

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random

HOST = '192.168.1.99'
PORT = 3333

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        data = self.prepare_data("No Motion")
        self.wfile.write(data)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(f"Received POST request with data: {post_data.decode()}")

        if post_data.decode() == "Motion":
            data = self.prepare_data(post_data.decode())
        else:
            data = b"No Motion"

        self.send_response(200)
        self.end_headers()
        self.wfile.write(data)

    def prepare_data(self, data):
        if data == "Motion":
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            zone = random.randint(1, 3)
            data = f"ID: {random.randint(1000, 9999)}, Time: {current_time}, Zone: {zone}"
            return bytes(data, 'utf-8')
        else:
            return b"No Motion"

server = HTTPServer((HOST, PORT), Server)
print(f"Server now running at {HOST}:{PORT}")
server.serve_forever()
