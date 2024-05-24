from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import socket

HOST = '192.168.31.24'
PORT_AS_SERVER = 4444
PORT_AS_CLIENT = 3333
HOST_Server='192.168.30.97'

class RPi_HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                client = http.client.HTTPConnection(HOST, PORT_AS_CLIENT)
                client.request('GET', self.path)   
                response = client.getresponse()
                self.send_response(response.status)    
                for header, value in response.getheader():
                    self.send_header(header, value)
                self.end_headers()
                data = response.read()
                self.wfile.write(data)
                client.close()
        except Exception as e:
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
