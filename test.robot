*** Settings ***
Library     RequestsLibrary
Library     ClientSimulator.py           192.168.30.97        4444

*** Variables ***
${server_endpoint}       http://192.168.31.20:3333
${RPi_client_endpoint}   http://192.168.30.97:4444
${Client}                http://192.168.30.97:4444


*** Test Cases ***
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
    ${response} =    POST     ${RPi_client_endpoint}    data=motion
    Should Be Equal As Strings    ${response.status_code}    200
    Log    ${response.content}
Test Data From Client
    [Documentation]  Testing the data from the client 
    ${response} =      GET     ${Client}  data= motion
    Should Be Equal As Strings    ${response.status_code}    200