# import the necessary modules 
from http.server import BaseHTTPRequestHandler, HTTPServer # because the RPi i a server so i need to import http.server module
import http.client # and http.client module because it's going to be a client for the main server (Server_http.py)
HOST = '192.168.31.6'
HOST_Server='192.168.30.97' # but your static ip-adress here, than your client should listen for the IP 
PORT_AS_SERVER = 4444
PORT_AS_CLIENT = 3333
 

class RPi_HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Client functionality
            client = http.client.HTTPConnection(HOST, PORT_AS_CLIENT) # connect to the server "server_http" as client 
            client.request('GET', '/') # GET method
            response = client.getresponse() # get the response
            data = response.read().decode()# reading the response and save the response in data variable
            print(f'Received from Server: {data}') # writing what the server have sent to the RPi

            #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#  As a server   #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# 
            """""
            RPi as a server, we sending what we have received from the Main server to the client without doing anything with the data 

            """
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(data.encode())  # Sending back the received data to the client 
    # this function is taking the data from the client and send it forward to the Main server "Server_http.py" 
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        print(f'Received from client: {post_data}')

        # Forward the POST data to the CLient
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