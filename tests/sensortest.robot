#*************** TESTING ************** ########
############## Settings ############## 
#--------------------------- ############## Settings ############## -----------------------------
#  using the Requestslibrary, to test the man in the middle and the server throug the url        |
#------------------------------------------------------------------------------------------------
#  using Process library, to use the keywords that is available at this library like Run         |
# -----------------------------------------------------------------------------------------------
# using the Collections library, to get the log keyword in this library                          |
# -----------------------------------------------------------------------------------------------
#  using the SensorSimulatorLibrary, that  to meniblte data and send it to the man in the-middle |
# ------------------------------------------------------------------------------------------------
#   using the StoreTracker library to Start the StoreTracker server                              |
# ------------------------------------------------------------------------------------------------

# --------------------------  ############# Keywords ############# -------------------------------
# Start Server, to start the Store tracker  i needed to use the process library  and Start the Pro|
# ------------------------------------------------------------------------------------------------
# Store Tracker Start, this one is calling the Start method of the StoreTrackerLibrary.py         |
# ------------------------------------------------------------------------------------------------
# Stop Server use it to Terminate the process  which i started in the Start Server                |
# ------------------------------------------------------------------------------------------------
# Sending Right Data here i'm using the SensorSimulatorLibrary Send data metod to send the data   |
# ------------------------------------------------------------------------------------------------
# Check Server Response, checking if the Store tracker is sending any response to the  using the Get|
# ---------------------------------------------------------------------------------------------------
# Check The Man In The Middle Response using both Get and POST to test the Response from the RPi    |
#  -------------------------------------------------------------------------------------------------
# ---------------------------- ############ TEST CASE ########### ----------------------------------|
# I chosed to to one Test case which contain all the Keyword which i have so i Start with the first |
# keyword, which was to start the Store Tracker, for more info take a look at the StoreTrackerLibrary|
# after that so i start the process using the keyword Start Server when i did these all so i seed the|
# data using the keyword Sending Right Data to send the Live_data virable to the RPi and the Store   |
# tracker, than i Check the response from the man in the meddle using the both GET and POST methods  |
# after that so i jsut terminate the process  and send a log if the Start and stop test case is done |
#----------------------------------------------------------------------------------------------------

*** Settings ***
Library     RequestsLibrary
Library     Process
Library     Collections
Library      ../Library/SensorSimulatorLibrary.py   192.168.30.97    4444
Library      ../Library/StoreTrackerLibrary.py

*** Variables ***
${server_endpoint}       http://192.168.31.24:3333
${RPi_client_endpoint}   http://192.168.30.97:4444
${man_in_the_Middle}     http://192.168.31.24:3333
${live_data}  {"frames":[{"events":[{"type":"motion","attributes":{"Event Type":"Enter Line","geometry_name":"sco 1","Event End":"Exit Line"}}]}]} 

*** Keywords ***
Start Server
    [Documentation]    Start the server in a separate process.
    Start Process    python    Store_tracker     alias=server    shell=True
Store Tracker Start
    [Documentation]    The Store tracker is running .
    Start Store Tracker 
Stop Server
    [Documentation]    Stop the server process.
    Terminate Process    server
Sending Right Data
    [Arguments]    ${data}
    Send Data    ${data}
Wait For Server To Be Ready
    [Documentation]    Wait for the server to be ready to accept connections.
    Wait Until Keyword Succeeds    10x    2s    Check Server Response


Check Server Response
    [Documentation]    Check if the server responds to a GET request.
    ${response} =    GET    ${server_endpoint}
    Should Be Equal As Strings    ${response.status_code}    200
Check The Man In The Middle Response
    [Documentation]    Check if the server responds to a GET request.
    ${response} =    GET    ${RPi_client_endpoint}
    Should Be Equal As Strings    ${response.status_code}    200
Check The Man In The Middle Response with POST request
    [Documentation]    Check if the server responds to a POST request.
    ${response} =    POST    ${RPi_client_endpoint}    ${live_data}
    Should Be Equal As Strings    ${response.status_code}    200
    Log    ${response.content}
*** Test Cases ***
Start and Stop Server
    [Documentation]    Test to start Store_tracker App and that the server stops  after 5 seconds of runtime. 
    Store Tracker Start
    Start Server    
    Sending Right Data    ${live_data}
    Check The Man In The Middle Response
    Check The Man In The Middle Response with POST request
    Check Server Response
    Sleep    1s
    Stop Server
    Log    Server started and stopped successfully.

##### this test is just for Omar and Robert #################
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
    Sending Right Data     ${live_data}
    ${motion_response} =    POST   ${RPi_client_endpoint}/motion    ${live_data}
    Should Be Equal As Strings    ${motion_response.status_code}    200

##### this test is just for Omar and Robert #################
#     ${no_motion_response} =    POST    ${RPi_client_endpoint}/motion    json={"event": "no motion"}
#     Should Be Equal As Strings    ${no_motion_response.status_code}    200
#     Should Contain    ${no_motion_response.content}    "No data to send"
##### this test is just for Omar and Robert #################
# Test Zone Names in Events
#     [Documentation]    Test to ensure that motion events correctly include predetermined zone names.
#     @{zones} =    Create List        sco 1    sco 2    sco 3    sco 4    Exit Gate
