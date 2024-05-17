# import threading
# from robot.api.deco import keyword
# import json
# from SensorSimulator import SensorSimulator

# class SensorSimulatorLibrary:
#     def __init__(self, host='192.168.30.97', port=4444):
#         self.client_simulator = SensorSimulator(host, port)

#     @keyword
#     def Start_Sensor(self):
#         motion_thread = threading.Thread(target=self.client_simulator.generate_motion_data)
#         motion_thread.start()


#     @keyword
#     def send_data(self, data):
#         self.client_simulator.send_data(json.loads(data))
#     @keyword
#     def send_custom_data(self, data):
#         self.client_simulator.generate_motion_data()

import threading
import json
from robot.api.deco import keyword
from SensorSimulator import SensorSimulator

class SensorSimulatorLibrary:
    def __init__(self, host='192.168.30.97', port=4444):
        self.client_simulator = SensorSimulator(host, port)

    @keyword
    def start_sensor(self):
        motion_thread = threading.Thread(target=self.client_simulator.generate_motion_data)
        motion_thread.daemon = True  # Ensure the thread closes when the main program exits
        motion_thread.start()

    @keyword
    def send_data(self, data):
        self.client_simulator.send_data(json.loads(data))

    @keyword
    def send_custom_data(self, data):
        self.client_simulator.send_data(json.loads(data))

# You may also add a method to stop the sensor if needed
