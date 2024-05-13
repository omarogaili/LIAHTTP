#this klass will send data to the server motion and no motion if the server get motion 
## then the server will send back a id and a ask the server in which zone the motion was detected

import http.client
import time
import random
import threading

class ClientSender(http.client.HTTPConnection):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.motion = ['motion', 'no motion']
        self.modified_data = None
        self.zone = None

    def motion_detection(self):
        while True:
            self.modified_data = random.choice(self.motion)
            # self.zone = random.randint(1, 3)
            self.request('POST', '/', body=str(self.modified_data) , headers={"Host": self.host, "Content-Type": "text/plain"})
            response = self.getresponse()
            if response.status == 200:
                data = response.read().decode()
                print(f"Received from server: {data}")
            else:
                print("Server error")
            time.sleep(5)

class ClientReceiver(http.client.HTTPConnection):
    def __init__(self, host, port):
        super().__init__(host, port)

    def do_GET(self):
        self.request('GET', '/', headers={"Host": self.host})
        response = self.getresponse()
        data = response.read().decode()
        print(f" Received: {data}")

def main():
    host = '192.168.30.97'
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
