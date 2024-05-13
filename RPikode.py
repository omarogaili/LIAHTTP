from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client

HOST = '192.168.31.20'
PORT_AS_SERVER = 4444
PORT_AS_CLIENT = 3333
HOST_Server='192.168.30.97'

class RPi_HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            client = http.client.HTTPConnection(HOST, PORT_AS_CLIENT)
            client.request('GET', '/')   
            response = client.getresponse()
            data = response.read().decode()
            print(f'Received from Server: {data}')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(data.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        print(f'Received from client: {post_data}')

        client = http.client.HTTPConnection(HOST, PORT_AS_CLIENT)
        client.request('POST', '/', body=post_data.encode())
        response = client.getresponse()
        client_response_data = response.read().decode()
        client.close()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(client_response_data.encode())  

def run_server():
 server = HTTPServer((HOST_Server, PORT_AS_SERVER), RPi_HTTPHandler)
 print(f"Server now running at {HOST_Server}:{PORT_AS_SERVER}")
 server.serve_forever()

if __name__ == "__main__":
    run_server()
