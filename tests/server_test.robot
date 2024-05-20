# in this test i use the server.py file to test if we  have any connection between the  server and the RPi.
#by using the opratingSystem and the Process libraries

# test number one starting the server.py, by using process library, the Keyword Run Process and the language we using and the name of the file and alias server
# test number two testing if we have a response from the server did we get a response with 200 
# test number three testing if we have any response from the RPi did we get a response with 200 
# test number four testing if we send data to the RPi did we get it forward to the RPi. in this test we are the client and we sending motion to the RPi. what i want to test is :
## 1. if the RPi get this data.
## 2. if the RPi send this data forward to the Server
# what we can do to make this test more compliet is to test if this data was sent to the server. because now i start the server.py and when i run this test i open the server.py terminal and wait until i get a motion in the server.py terminal 
# than i know if the RPi send motion to the server.py. 
# ******* Problems with this test *******
# i could not stop the server and that is an issue because if we cant stop the server from running than we cant  start the server from the Python file.


*** Settings ***
Library     OperatingSystem
Library     RequestsLibrary
Library     Process

*** Variables ***
${server_endpoint}     http://192.168.31.20:3333
${RPi_client_endpoint}   http://192.168.30.97:4444

*** Test Cases ***
*** Test Cases ***
Start and Stop Server
    [Documentation]    Test to start and stop the server
    Run Process    python    Server.py    shell=True    alias=server    timeout=10s


Test Successful Response from Server
    [Documentation]    Test to verify successful response from the server
    ${response} =    GET    ${server_endpoint}   
    Should Be Equal As Strings    ${response.status_code}    200 
    Log    ${response.content}     

Test Successful Communication with RPi Client
    [Documentation]    Test to verify successful communication with RPi client
    ${response} =    GET   ${RPi_client_endpoint}
    Should Be Equal As Strings    ${response.status_code}    200 
    Log    ${response.content}   

Test Motion Detection
    [Documentation]    Test motion detection functionality
    ${response} =    POST    ${RPi_client_endpoint}    data=motion
    Should Be Equal As Strings    ${response.status_code}    200
    Log    ${response.content}