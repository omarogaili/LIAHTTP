# # #this klass will send data to the server motion and no motion if the server get motion 
# # ## then the server will send back a id and a ask the server in which zone the motion was detected
import http.client
import time
import random
import threading
import json
import uuid

class SensorSimulator(http.client.HTTPConnection):
    """
    This class simulates a sesame sensor. It generates and sends mocked customer flow data to the store tracker app.
    """
    
    def __init__(self, host, port):
        super().__init__(host, port)
        self.sensor_state = None
        self.motion_types = 'motion'
        self.Enter_Line = 'Enter Line'
        self.Exit_Line = 'Exit Line'
        self.zones = ['sco 1', 'sco 2', 'sco 3', 'sco 4', 'Exit Gate']
        self.track_id = None
        self.stop_event = threading.Event()
# this method is creating a data and sending it to the store tracker as a json object
    def generate_motion_data(self):
        while not self.stop_event.is_set(): # create a loop to generate and send different data to the store tracker
            zone_name = random.choice(self.zones) # get a random zone name 
            track_id = str(uuid.uuid4()) # get a random and unique ID for the motion which has been detected 
            if self.sensor_state == 1: # if the state of the sensor is 1 than we have a motion, and in this way so we are sending this data below 
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
            else: # otherwise if the state is 0 so send there is no motion
                live_data = {"message": "no motion"}

            self.send_data(live_data)
            time.sleep(5) # send this data every 5 sec
# this method is create to send the data which we have create in the method above to the Man in the middle and (store tracker)
    def send_data(self, data):
        try:
            self.request('POST', '/', body=json.dumps(data), headers={"Content-Type": "application/json"})
            response = self.getresponse()
            if response.status == 200:
                response_data = response.read().decode()
                print(f"Received from server: {response_data}")
            else:
                print("Server error")
        except (http.client.HTTPException, ConnectionResetError) as e:
            print(f'Connection error :{e}')
            self.reconnect()
        except Exception as e:
            print(f'Unexpected error :{e}')
    #in the reconnect method so i try to reconnect the sensor again to the RPi if the connection is last. 
    # so long we don't have the the stop event set than the reconnect method will try to reconnect
    # its just like restart the sensor, and trying to connect again
    def reconnect(self):
        print("trying to reconnect...")
        while not self.stop_event.is_set():
            try:
                self.close() 
                self.connect()
                print("Reconnected successfully")
                return
            except (http.client.HTTPException, ConnectionRefusedError) as e:
                print(f"Reconnection failed: {e}")
                time.sleep(5) # wait 5 seconds before trying reconnect again 
            except Exception as e:
                print(f"Unexpected error during reconnection: {e}")
                time.sleep(5) # wait 5 seconds before trying to reconnect again
# stop method for the Sensor (useful to run a test for the sensor!)
    def stop(self):
        self.stop_event.set()
# a Main method, using thread to run the generate method
def main():
    host = '192.168.30.97'
    port = 4444
    client_simulator = SensorSimulator(host, port)
    motion_thread = threading.Thread(target=client_simulator.generate_motion_data) 
    motion_thread.start()
    
    return client_simulator, motion_thread

if __name__ == "__main__":
    try:
        client_simulator, motion_thread = main()
        while True:
            time.sleep(1)# you need to wait for the sensorSimulator to be shut down (to complete the generation!) 
    except KeyboardInterrupt:
        print("Shutting down the server")
        client_simulator.stop()
        motion_thread.join()
        print('Sensor Simulation has been stopped')
