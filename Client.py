# import http.client

# class Client(http.client.HTTPConnection):
#     def __init__(self, host, port):
#         super().__init__(host, port)

#     def do_GET(self):
#         self.request('GET', '/', headers={"Host": self.host})
#         response = self.getresponse()
#         data = response.read().decode()
#         print(f"{response.status} {response.reason} ,Received: {data}")
#         modified_data = self.update_data_with_addition(data)  # call the update_data method here
#         self.send_back_to_server(modified_data)  # send back the result to the server through the send_back_to_server method

#     def update_data_with_addition(self, data):
#         data_parts = data.split(', ')
#         zone = int(data_parts[-1].split(': ')[-1])
#         if zone == 3:
#             return "open gate"
#         else:
#             return "do not open"

#     def send_back_to_server(self, modified_data):
#         self.request('POST', '/', body=str(modified_data), headers={"Host": self.host})
#         response = self.getresponse()

# HOST = '192.168.31.10'
# PORT = 4444
# client = Client(HOST, PORT)
# client.do_GET()
# import http.client
# import time
# import random

# class MotionSensorClient:
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port
#         self.client = http.client.HTTPConnection(self.host, self.port)
#         self.motion= ["Motion", "No Motion"]

#     def detect_motion(self):
#         while True:
#             rand_value= random.choice(self.motion)
#             self.client.request('GET', '/', rand_value)
#             response = self.client.getresponse()
#             data = response.read().decode()
#             print(f"Response from the server: {data}. Sending back to the server: {rand_value}")

#             time.sleep(5)

# if __name__ == "__main__":
    
#     HOST = '192.168.1.99'
#     PORT = 4444
#     motion_sensor = MotionSensorClient(HOST, PORT)
#     motion_sensor.detect_motion()
# HOST = '192.168.31.10'


import http.client
import time
import random

class MotionSensorClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = http.client.HTTPConnection(self.host, self.port)
        self.motion= ["Motion", "No Motion"]

    def detect_motion(self):
        while True:
            rand_value= random.choice(self.motion)
            self.client.request('GET', '/', rand_value)
            response = self.client.getresponse()
            data = response.read().decode()
            print(f"Response from the server: {data}. Sending back to the server: {rand_value}")

            time.sleep(5)

if __name__ == "__main__":
    
    HOST = '192.168.1.155'
    PORT = 4444
    motion_sensor = MotionSensorClient(HOST, PORT)
    motion_sensor.detect_motion()
