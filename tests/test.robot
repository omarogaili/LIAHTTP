*** Settings ***
Library     RequestsLibrary
# Library     ClientSimulator.py           192.168.30.97        4444

*** Variables ***
${server_endpoint}       http://192.168.31.20:3333
${RPi_client_endpoint}   http://192.168.30.97:4444



*** Test Cases ***
Verify Successful Response from Sensor
    [Documentation]    Test to verify successful response from sensor
    ${response} =    GET    ${server_endpoint}
    Should Be Equal As Strings    ${response.status_code}    200 
    Log    ${response.content}

Verify Successful Communication with ManInTheMiddle
    [Documentation]    Test to verify successful communication with ManInTheMiddle
    ${response} =    GET   ${RPi_client_endpoint}
    Should Be Equal As Strings    ${response.status_code}    200 
    Log    ${response.content}

Verify Sensor Motion Detection
    [Documentation]    Test to verify Sensor motion detection functionality
    ${response} =    POST     ${RPi_client_endpoint}    data=motion
    Should Be Equal As Strings    ${response.status_code}    200
    Log    ${response.content}
Verify Data From Sensor To ManInTheMiddle
    [Documentation]  Test to assert data being sent from sensor to ManInTheMiddle is unaltered
    ${response} =      GET     ${RPi_client_endpoint} data= motion
    Should Be Equal As Strings    ${response.status_code}    200