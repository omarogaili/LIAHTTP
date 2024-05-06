*** Settings ***
Library     RequestsLibrary
# Library      Client.py    http.client.HTTPConnection

*** Variables ***
${endPoint}     http://192.168.31.10:3333 
${RPi_client}   http://192.168.31.10:4444
${Client}       http://192.168.31.10:4444

*** Test Cases ***
Test Successful Response from Server
    [Documentation]    Test to verify successful response from the server
    ${response} =    Get   ${endPoint}
    Should Be Equal As Strings  ${response.status_code}    200 
    Log    ${response.content}     

Test Successful Communication with RPi Client
    [Documentation]    Test to verify successful communication with RPi client
    ${response} =    Get   ${RPi_client}
    Should Be Equal As Strings  ${response.status_code}    200 
    Log    ${response.content}   

Test Zone 3 Handling in Client
    [Documentation]    Test to verify handling of Zone 3 in client
    ${response} =    Get     ${RPi_client}  
    Log    ${response.text}
    Should Be Equal As Strings  ${response.content}    open gate   
Test Zone 1 or 2 Handling in Client
    [Documentation]    Test to verify handling of Zone 1 or Zone 2 in client
    ${response} =    Get   ${RPi_client}
    Should Be Equal As Strings  ${response.content}    do not open 