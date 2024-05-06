*** Settings ***
Library     RequestsLibrary

*** Variables ***
${endPoint}     http://192.168.1.240:3333 
${response}
${RPi_client}   http://192.168.30.97:4444

*** Test Cases ***
Test 1
    ${response} =    Get   ${endPoint}
    #in the test blow i check if I get a response from the server
    Should Be Equal As Strings  ${response.status_code}    200 
    Log    ${response.content}        # Eller innehållet i svaret
    Should Be Equal As Strings    ${response.content}   8  # using Should be Equal As Strings and  response.content  to check if the server sending 8 as i expected

Test 2
    ${response} =    Get   ${RPi_client}
    Log    ${response.status_code}    # Du kan logga statuskoden om
    Log    ${response.content}        # Eller innehållet i svaret