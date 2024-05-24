from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import socket
# ! --------------------------------------------------------------------------------------------------------------------|
# * in this class so I create a HTTP-server, which is lyssning to a specific IP and PORT. those are HOST_server and     |
# * PORT_AS_Server. So you may change those to the HOST_server and the PORT_as_server you need, you can also change the |
# * HOST and the PORT to the Store Tracker IP and PORT. In this script all we do is  when the man in the middle server  |
# *  get a GET or a POST request, it's send it forword to the "Main Server" which is using HOST and PORT_AS_Client      |
# *  and when the server send some data, this data will be forword sended to the client as will                         |
# !---------------------------------------------------------------------------------------------------------------------  


HOST = '192.168.31.24'
PORT_AS_CLIENT = 3333
HOST_Server='192.168.30.97'
PORT_AS_SERVER = 4444

class RPi_HTTPHandler(BaseHTTPRequestHandler):
    # ! in do_GET method so we create a get request. create a connection with the "Main Server", get the response from the Main server and send it to the Client
    def do_GET(self):
        try:
            if self.path == '/': #*   make a connection with just specific request. you can change it if you wont to response to all the requests  
                client = http.client.HTTPConnection(HOST, PORT_AS_CLIENT) #! create an Connection with the "Main Server"
                client.request('GET', self.path) 
                response = client.getresponse()
                self.send_response(response.status)    
                for header, value in response.getheader(): 
                    self.send_header(header, value) #! sending the header from the response which i get from the "Main Server"
                self.end_headers()
                data = response.read()
                self.wfile.write(data)
                client.close()
        except Exception as e: #! Exception handling 
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Internal error: {str(e)}'.encode())
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print(f'Received from client: {post_data}')
            client = http.client.HTTPConnection(HOST, PORT_AS_CLIENT)
            client.request('POST', self.path, body=post_data, headers=self.headers)
            response = client.getresponse()
            self.send_response(response.status)
            for header, value in response.getheaders():
                self.send_header(header, value)
            self.end_headers()
            data= response.read()
            self.wfile.write(data)
            client.close()
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Internal error: {str(e)}'.encode())

def run_server():
    try:
        server= HTTPServer((HOST_Server,PORT_AS_SERVER), RPi_HTTPHandler)
        print(f"Server now running at {HOST_Server}:{PORT_AS_SERVER}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down the server")
        server.socket.close()
    except socket.error as e:
        print(f'Socket error: {str(e)}')
        server.socket.close()
    except Exception as e:
        print(f'Unexpected error :{e}')
    finally:
        try:
            server.server_close()
        except Exception as e:
            print(f'Unexpected error :{e}')

if __name__ == "__main__":
    run_server()
