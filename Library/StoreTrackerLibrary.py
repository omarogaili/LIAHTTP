import threading
from http.server import HTTPServer
from src.Store_tracker import Store_tracker, start_server
# I use this class to start the Store Tracker when i Start the test in Robot Framework 
# this class is using threading to gave the Store tracker a permission to start in a separate resource 
# what i need to send in start method is the IP and port  that the Store Tracker is running at "Should running at".
class StoreTrackerLibrary:
    def __init__(self):
        self.server_thread = None
        self.server = None

    def start_store_tracker(self):
        """
        Starts the Store Tracker server in a separate thread.
        """
        self.server = HTTPServer(('192.168.31.24', 3333), Store_tracker)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        print("Server started")
