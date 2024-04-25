from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = '10.247.162.50'
PORT = 3333
Message= b'8'

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(Message)
# do_POSt to read the response what the client is sending back to the server
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        # post_data = self.rfile.read(content_length)
        # Message= post_data
        Message= self.reading_the_response(content_length)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'POST request received with data: ' + Message)
        print(Message)

# vad händer om massage inte ändras?! då  måste jag skicka tillbaka massage som
    def reading_the_response(self,content_length):
        post_data = self.rfile.read(content_length)
        Message=bytes(post_data)
        return Message

server = HTTPServer((HOST, PORT), Server)
print(f"Server now running at {HOST}:{PORT}")
server.serve_forever()
print(Message)
