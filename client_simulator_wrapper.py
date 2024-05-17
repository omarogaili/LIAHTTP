
import SensorSimulator

class ClientSimulatorWrapper:
    def __init__(self, host, port):
        self.client_simulator = SensorSimulator(host, port)

    def start_simulation(self):
        self.client_simulator.start()


