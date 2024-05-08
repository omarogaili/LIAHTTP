import http.client
import time
import random
import threading

import http.client
import time
import random
import threading

class ClientSender(http.client.HTTPConnection):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.motion = ['motion', 'no motion']
        self.modified_data = None

    def motion_detection(self):
        while True:
            self.modified_data = random.choice(self.motion)
            self.request('POST', '/', body=str(self.modified_data), headers={"Host": self.host})
            response = self.getresponse()
            print(f"Sent: {self.modified_data}")
            time.sleep(5)

class ClientReceiver(http.client.HTTPConnection):
    def __init__(self, host, port):
        super().__init__(host, port)

    def do_GET(self):
        self.request('GET', '/', headers={"Host": self.host})
        response = self.getresponse()
        data = response.read().decode()
        print(f"{response.status} {response.reason}, Received: {data}")

def main():
    host = '192.168.1.155'  
    port = 4444  

    sender = ClientSender(host, port)
    receiver = ClientReceiver(host, port)

    motion_thread = threading.Thread(target=sender.motion_detection)
    motion_thread.start()

    while True:
        receiver.do_GET()
        time.sleep(1)  

if __name__ == "__main__":
    main()

