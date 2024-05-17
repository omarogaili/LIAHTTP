import SensorSimulator
class NoMotionsimulator:
    def __init__(self):
        self.message= "no motion"
    def simulate_no_motion(self):
        client= SensorSimulator()
        client.send_data(self.message)