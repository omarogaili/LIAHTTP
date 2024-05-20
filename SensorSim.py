
import threading
import src.SensorSimulator as SensorSimulator

def start_sensor_simulation():
    host = '192.168.30.97'
    port = 4444
    client_simulator = SensorSimulator(host, port)
    motion_thread = threading.Thread(target=client_simulator.generate_motion_data)
    motion_thread.start()
    return client_simulator, motion_thread