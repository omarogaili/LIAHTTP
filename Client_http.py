import http.client

class Client(http.client.HTTPConnection):
    def __init__(self, host, port):
        super().__init__(host, port)

    def do_GET(self):
        self.request('GET', '/', headers={"Host": self.host})
        response = self.getresponse()
        data = response.read().decode()
        print(f"{response.status} {response.reason} ,Received: {data}")
        modified_data = self.update_data_with_addition(data) # call the update_data method here
        self.send_back_to_server(modified_data) # send back the result to the server through the send_back_to_server method 
    # taking the data which we get from the server and do something with it here. and returning the value
    def update_data_with_addition(self, data):
        result = int(data) + 10
        print(f"The data after add function is: {result}")
        return result

    def send_back_to_server(self, modified_data):
        self.request('POST', '/', body=str(modified_data), headers={"Host": self.host})
        response = self.getresponse()

HOST = '10.170.118.144'
PORT = 4444
client = Client(HOST, PORT)
client.do_GET()
