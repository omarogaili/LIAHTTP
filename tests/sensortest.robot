
*** Settings ***
Library     OperatingSystem
Library     RequestsLibrary
Library     Process
Library     Collections
Library     NoMotionsimulator.py
*** Variables ***
${server_endpoint}       http://192.168.31.20:3333
${RPi_client_endpoint}   http://192.168.30.97:4444

*** Keywords ***
Start Server
    [Documentation]    Start the server in a separate process.
    Run Process    python    Store_tracker.py   alias=server    shell=True

Stop Server
    [Documentation]    Stop the server process.
    Terminate Process    server

Wait For Server To Be Ready
    [Documentation]    Wait for the server to be ready to accept connections.
    Wait Until Keyword Succeeds    10x    2s    Check Server Response

Check Server Response
    [Documentation]    Check if the server responds to a GET request.
    ${response} =    GET    ${server_endpoint}
    Should Be Equal As Strings    ${response.status_code}    200

*** Test Cases ***
Start and Stop Server
    [Documentation]    Test to start Store_tracker App and that the server stops  after 5 seconds of runtime. 
    Start Server
    Wait For Server To Be Ready
    Sleep    5s
    Stop Server
    Log    Server started and stopped successfully.

# Test Successful Response from Server
#     [Documentation]    Test to verify successful response from the server.
#     ${response} =    GET    ${server_endpoint}
#     Should Be Equal As Strings    ${response.status_code}    200 
#     Log    ${response.content}

# Test Sensor No Motion State
#     [Documentation]    Test to verify sensor maintains 'no motion' state and does not trigger false motion events.
#     # Simulate No Motion    30 minutes
#     ${response} =    NoMotionsimulator.simulate_no_motion
#     # ${no_motion_detected} =    Check Sensor State
#     # Should Be True    ${no_motion_detected}
#     Should Be Equal As Strings    ${response}     no motion
#     Log    Sensor maintained no motion state for 30 minutes without false triggers


Test Motion Detection Events
    [Documentation]    Test correct handling of events created in sensor states 'motion' and 'no motion'.
    ${motion_response} =    POST    ${RPi_client_endpoint}/motion    json={"event": "motion", "track_id": "1234", "zone": "Enter Line"}
    Should Be Equal As Strings    ${motion_response.status_code}    200
    Should Contain    ${motion_response.content}    "motion"

#     ${no_motion_response} =    POST    ${RPi_client_endpoint}/motion    json={"event": "no motion"}
#     Should Be Equal As Strings    ${no_motion_response.status_code}    200
#     Should Contain    ${no_motion_response.content}    "No data to send"


# Test Zone Names in Events
#     [Documentation]    Test to ensure that motion events correctly include predetermined zone names.
#     @{zones} =    Create List        sco 1    sco 2    sco 3    sco 4    Exit Gate
