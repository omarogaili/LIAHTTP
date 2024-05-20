import threading
from robot.api.deco import keyword
import json
import sys

sys.path.insert(1, '/home/omar/Desktop/Desktop-omar/Sesame2-sim/src/SensorSimulator.py')

from src.SensorSimulator import SensorSimulator
#this class is the Library class for robot Framework, i use't to test those functions. 
# what I test in this class is :
## 1. the first test is to start the SensorSimulator and wait for the response from the RPi and the Store tracker
## 2. the second test is to send i Data to the RPi. 
class SensorSimulatorLibrary:
    """
    SensorSimulatorLibrary class
    """
    def __init__(self, host='192.168.30.97', port=4444):
        self.client_simulator = SensorSimulator(host, port)

    @keyword
    def Start_Sensor(self):
        motion_thread = threading.Thread(target=self.client_simulator.generate_motion_data)
        motion_thread.start()


    @keyword
    def send_data(self, data):
        try:
            parsed_data = json.loads(data)
            geometry_name = parsed_data['frames'][0]['events'][0]['attributes']['geometry_name']
            if geometry_name in self.client_simulator.zones:
                self.client_simulator.send_data(parsed_data)
            else:
                raise ValueError(f"Invalid geometry_name: {geometry_name}")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error sending data: {e}")
            raise


