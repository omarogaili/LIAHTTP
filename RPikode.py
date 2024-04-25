# import the necessary modules 
from http.server import BaseHTTPRequestHandler, HTTPServer # because the RPi i a server so i need to import http.server module
import http.client # and http.client module because it's going to be a client for the main server (Server_http.py)
HOST = '10.247.162.50'
PORT_AS_SERVER = 4444
PORT_AS_CLIENT = 3333


# *#*#*#*#*#*#*#*#*#*##*#*#*#*#*#*#*# Client Side of the RPi   #*#*#*#*#*#*#*#*#*##*#*#*#*#*#*#*#*#*#*##*#*#*#*#*#*#*#*#*#*#
# class RPi_client_side(http.client.HTTPConnection):
#     def __init__(self, host, port):
#         super().__init__(host, port)

#     def do_GET(self):
#         self.request('GET', '/', headers={"Host": self.host})
#         response= self.getresponse()
#         data= response.read().decode()
#         print(f'Received: {data}')
# # the class below is the server side in RPi so what this class is going to do is manage the GET and POST requests from the client to the server

# class RPi_server_side(BaseHTTPRequestHandler):
#     def __init__(self):
#         self.client = RPi_client_side

#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(self.client)

# client= RPi_client_side(HOST, PORT_AS_CLIENT)
# client.do_GET()

# server = HTTPServer((HOST, PORT_AS_SERVER), RPi_server_side)
# print(f"Server now running at {HOST}:{PORT_AS_SERVER}")
# server.serve_forever()

# from http.server import BaseHTTPRequestHandler, HTTPServer
# import http.client

# HOST = '10.247.162.50'
# PORT_AS_SERVER = 4444
# PORT_AS_CLIENT = 3333

# class RPi_client_side(http.client.HTTPConnection):
#     def __init__(self, host, port):
#         super().__init__(host, port)

#     def do_GET(self):
#         self.request('GET', '/', headers={"Host": self.host})
#         response = self.getresponse()
#         data = response.read().decode()
#         print(f'Received: {data}')
#         return data

# class RPi_server_side(BaseHTTPRequestHandler):
#     def __init__(self, request, client_address, server, client_data):
#         self.client_data = client_data
#         super().__init__(request, client_address, server)

#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(self.client_data)

# client = RPi_client_side(HOST, PORT_AS_CLIENT)
# client_data = client.do_GET()

# server = HTTPServer((HOST, PORT_AS_SERVER), RPi_server_side)
# server.client_data = client_data
# print(f"Server now running at {HOST}:{PORT_AS_SERVER}")
# server.serve_forever()
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client

HOST = '10.247.162.50'
PORT_AS_SERVER = 4444
PORT_AS_CLIENT = 3333

class RPi_HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Client functionality
            client = http.client.HTTPConnection(HOST, PORT_AS_CLIENT)
            client.request('GET', '/')
            response = client.getresponse()
            data = response.read().decode()
            print(f'Received from Server: {data}')

            # Server functionality
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(data.encode())  # Sending back the received data to the client

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        print(f'Received from client: {post_data}')

        # Forward the POST data to the client
        client = http.client.HTTPConnection(HOST, PORT_AS_CLIENT)
        client.request('POST', '/', body=post_data.encode())
        response = client.getresponse()
        client_response_data = response.read().decode()
        client.close()

        # Send the client's response back to the original client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(client_response_data.encode())

def run_server():
    server = HTTPServer((HOST, PORT_AS_SERVER), RPi_HTTPHandler)
    print(f"Server now running at {HOST}:{PORT_AS_SERVER}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()









# import the necessary modules 
# from http.server import BaseHTTPRequestHandler, HTTPServer # because the RPi i a server so i need to import http.server module
# import http.client # and http.client module because it's going to be a client for the main server (Server_http.py)
# HOST = '10.247.162.50'
# PORT_AS_SERVER = 4444
# PORT_AS_CLIENT = 3333
# # the class below is the server side in RPi so what this class is going to do is manage the GET and POST requests from the client to the server
# class RPi_server_side(BaseHTTPRequestHandler):
#  class RPi_server_side(BaseHTTPRequestHandler):
#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length).decode()
#         print(f"Received: {post_data}")
        
#         conn_server = http.client.HTTPConnection(HOST, PORT_AS_CLIENT)
#         conn_server.request('POST', '/', post_data.encode())
        
#         response_server = conn_server.getresponse()
#         server_data = response_server.read()
#         print(f'Response from server: {server_data.decode()}')
        
#         conn_server.close()
        
#         self.send_response(200)
#         self.end_headers()
#         self.wfile.write(b'POST request received and transferred successfully to Server_http.py')

# def run_serverRPi():
#         server_address= ('', PORT_AS_SERVER)
#         server= HTTPServer(server_address,RPi_server_side)
#         print(f'RPi running at {PORT_AS_SERVER}')
#         server.serve_forever()
# if __name__ == '__main__':
#         run_serverRPi()

# server= RPi_server_side(HOST,PORT_AS_SERVER)