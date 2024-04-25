import http.client

class Client(http.client.HTTPConnection):
    def __init__(self, host, port):
        super().__init__(host, port)

    def do_GET(self):
        self.request('GET', '/', headers={"Host": self.host})
        response = self.getresponse()
        data = response.read().decode()
        print(f"{response.status} {response.reason} ,Received: {data}")
        modified_data = self.addition_to_the_data(data)
        self.send_back_to_server(modified_data)
        
    def addition_to_the_data(self, data):
        result = int(data) + 10
        print(f"The data after add function is: {result}")
        return result

    def send_back_to_server(self, modified_data):
        self.request('POST', '/', body=str(modified_data), headers={"Host": self.host})
        response = self.getresponse()
        # print(f"Sent modified data to server. Response: {response.status} {response.reason}")

HOST = '10.247.162.50'
PORT = 4444

client = Client(HOST, PORT)
client.do_GET()
