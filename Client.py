import http.client
import time 
import random
import threading
import asyncio
class Client(http.client.HTTPConnection):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.motion=['motion', 'no motion']
        self.modified_data= None

    def do_GET(self):
        self.request('GET', '/', headers={"Host": self.host})
        response = self.getresponse()
        data = response.read().decode()
        print(f"{response.status} {response.reason} ,Received: {data}")
        # self.motion_detection(self.motion, self.modified_data)

    def motion_detection(self):
            while True:
                self.modified_data= random.choice(self.motion)
                self.request('POST', '/', body=str(self.modified_data), headers={"Host": self.host})
                response = self.getresponse()
                time.sleep(5)
HOST = '192.168.30.97'
PORT = 4444
client = Client(HOST, PORT)
client.do_GET()
t1= threading.Thread(target=client.do_GET())
t1.start()
t1.join()
client.motion_detection()
