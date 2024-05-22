from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import json
import time
import socket

HOST = '192.168.31.24'
PORT_AS_SERVER = 4444
PORT_AS_CLIENT = 3333
HOST_Server='192.168.30.97'# Static IP, this IP. this what 

"""
This class acts as a ManInTheMiddle, that incercepts, monitors and forwards events/data between the SensorSimulator and Store>│
without altering or modifying any content.                                                                                   │
Neither the sensor or the store tracker app are aware that these monitoring activities are occurring.                        │
"""
class RPi_HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                client = http.client.HTTPConnection(HOST, PORT_AS_CLIENT)
                client.request('GET', '/')   
                response = client.getresponse()
                data = response.read().decode()
                print(f'Received from Server: {data}')
                self.send_response(response.status)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(data.encode())
        except Exception as e:
            self.send_response(500, f'Internal error:{str(e)}')

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            print(f'Received from client: {post_data}')
            client = http.client.HTTPConnection(HOST, PORT_AS_CLIENT)
            client.request('POST', '/', body=post_data.encode())
            response = client.getresponse()
            client_response_data = response.read().decode()
            client.close()
            self.send_response(response.status)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(client_response_data.encode())
        except json.JSONDecodeError:
            self.send_error(400, 'BAD Request JSON decode error')
        except Exception as e:
            self.send_error(500, f'Internal Error:{str(e)}')
def run_server():
    try:
        server = HTTPServer((HOST_Server, PORT_AS_SERVER), RPi_HTTPHandler)
        print(f"Server now running at {HOST_Server}:{PORT_AS_SERVER}")
        server.serve_forever()
    except KeyboardInterrupt:
            print("Shutting down the server")
            server.socket.close()
    except socket.error as e:
        print(f'Socket error: {str(e)}')
    except Exception as e:
        print(f'Unexpected error :{e}')
    finally:
        try:
            server.server_close()
        except Exception as e:
            print(f'Unexpected error :{e}')

if __name__ == "__main__":
    run_server()
