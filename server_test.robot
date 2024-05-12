*** Settings ***
Library     OperatingSystem
Library     RequestsLibrary
Library     Process

*** Variables ***
${server_endpoint}     http://192.168.1.99:5555
${RPi_client_endpoint}   http://192.168.1.155:4444

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