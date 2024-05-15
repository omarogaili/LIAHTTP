#this klass will send data to the server motion and no motion if the server get motion 
## then the server will send back a id and a ask the server in which zone the motion was detected

import http.client
import time
import random
import threading
import json

class ClientSender(http.client.HTTPConnection):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.motion = ['motion', 'no motion']
        self.modified_data = None
        self.zone = ['Enter Line', 'sco 1' , 'sco 2','sco 3', 'sco 4' ,'Exit Line' ]
        self.zone_name= None
        self.trackid= None
        self.no_event = 'No data to send'

    def motion_detection(self):
        while True:
            self.modified_data = random.choice(self.motion)
            self.zone_name = random.choice(self.zone)
            self.trackid = random.randint(1000, 9999)
            # self.request('POST', '/', body=str(self.modified_data) , headers={"Host": self.host, "Content-Type": "text/plain"})
            if(self.modified_data == 'motion'):
                live_data = {
                    'live_data': {
                        'frames': [
                            {
                                'events': [
                                    {
                                        'type': self.modified_data,
                                        'attributes': {
                                            'track_id': f'track id {self.trackid}',
                                            'geometry_name': f'Zone {self.zone_name}'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            elif self.modified_data == 'no motion':
                live_data = self.no_event

            self.request('POST', '/', body=str(live_data) , headers={"Host": self.host, "Content-Type": "json"})
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

    # def do_GET(self):
    #     self.request('GET', '/', headers={"Host": self.host})
    #     response = self.getresponse()
    #     data = response.read().decode()
    #     print(f" Received: {data}")
    def send_message(self, message):
        # Simulate sending message
        print("Simulating sending message...")
        print(json.dumps(message, indent=4))
        print("Message sent.")

def main():
    host = '192.168.30.97'
    port = 4444

    sender = ClientSender(host, port)
    receiver = ClientReceiver(host, port)

    motion_thread = threading.Thread(target=sender.motion_detection())
    motion_thread.start()

    while True:
        receiver.send_message(sender.modified_data())
        time.sleep(1)

if __name__ == "__main__":
    main()

