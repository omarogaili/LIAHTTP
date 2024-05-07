import http.client
import time 
import random
class Client(http.client.HTTPConnection):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.motion=['motion', 'no motion']

    def do_GET(self):
        self.request('GET', '/', headers={"Host": self.host})
        response = self.getresponse()
        data = response.read().decode()
        print(f"{response.status} {response.reason} ,Received: {data}")
        #modified_data = self.update_data_with_addition(data)  # call the update_data method here
        modified_data= self.motion_detection(self.motion)
        self.send_back_to_server(modified_data)  # send back the result to the server through the send_back_to_server method
    def motion_detection(self,motion):
            # while True:
            #     result = random.choice(motion)
            #     return result
            for i in self.motion:
                return random.choice(self.motion)
    
    # def update_data_with_addition(self, data):
    #     data_parts = data.split(', ')
    #     zone = int(data_parts[-1].split(': ')[-1])
    #     if zone == 3:
    #         return "open gate"
    #     else:
    #         return "do not open"


    def send_back_to_server(self, modified_data):
        while True:
            self.request('POST', '/', body=str(modified_data), headers={"Host": self.host})
            response = self.getresponse()
            time.sleep(10)

HOST = '192.168.30.97'
PORT = 4444
client = Client(HOST, PORT)
client.do_GET()
