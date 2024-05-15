# #this klass will send data to the server motion and no motion if the server get motion 
# ## then the server will send back a id and a ask the server in which zone the motion was detected
import http.client
import time
import random
import threading
import json
import uuid 

class ClientSimulator(http.client.HTTPConnection):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.sensor_state= None
        self.motion_types = 'motion'
        self.Enter_Line = 'Enter Line'
        self.Exit_Line = 'Exit Line'
        self.zones = ['sco 1', 'sco 2', 'sco 3', 'sco 4', 'Exit Gate']
        self.track_id = None

    def generate_motion_data(self):
        while True:
            self.sensor_state =  random.randint(0,1)
            motion_type = random.choice(self.motion_types)
            zone_name = random.choice(self.zones)
            track_id = str(uuid.uuid4())
            if self.sensor_state == 1:
                live_data = {
                    'live_data': {
                        'frames': [
                            {
                                'events': [
                                    {
                                        'type': self.motion_types,
                                        'attributes': {
                                            'track_id': track_id,
                                            'Event Type': self.Enter_Line,
                                            'geometry_name': zone_name,
                                            'Event End': self.Exit_Line
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            else:
                live_data = {"message": "no motion"}

            self.send_data(live_data)
            time.sleep(5)

    def send_data(self, data):
        self.request('POST', '/', body=json.dumps(data), headers={"Content-Type": "application/json"})
        response = self.getresponse()
        if response.status == 200:
            response_data = response.read().decode()
            print(f"Received from server: {response_data}")
        else:
            print("Server error")

def main():
    host = '192.168.30.97'
    port = 4444

    client_simulator = ClientSimulator(host, port)
    motion_thread = threading.Thread(target=client_simulator.generate_motion_data)
    motion_thread.start()

if __name__ == "__main__":
    main()
