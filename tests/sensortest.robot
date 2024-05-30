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

#! --------------------------  ############# Keywords ############# -------------------------------
#* Start Server, to start the Store tracker,  i needed to use the process library  and Start the Process|
# ------------------------------------------------------------------------------------------------
#* Store Tracker Start, this one is calling the Start method of the StoreTrackerLibrary.py              |
# ------------------------------------------------------------------------------------------------
#* Stop Server use it to Terminate the process  which i started in the Start Server                     |
# ------------------------------------------------------------------------------------------------
#* Sending The Sensor Data, here i'm using the SensorSimulatorLibrary Send data metod to send the data  |
# ------------------------------------------------------------------------------------------------
#* Check Server Response, checking if the Store tracker is sending any response  using the Get          |
# ---------------------------------------------------------------------------------------------------
# *Check The Man In The Middle Response using both Get and POST to test the Response from the RPi       |
#!  -------------------------------------------------------------------------------------------------
#! ---------------------------- ############ TEST CASE ########### ----------------------------------|
#* I chosed to to one Test case which contain all the Keyword which i have so i Start with the first |
#* keyword, which was to start the Store Tracker, for more info take a look at the StoreTrackerLibrary|
#* after that so i start the process using the keyword Start Server when i did these all so i seed the|
#* data using the keyword Sending Right Data to send the Live_data virable to the RPi and the Store   |
#* tracker, than i Check the response from the man in the meddle using the both GET and POST methods  |
#* after that so i jsut terminate the process  and send a log if the Start and stop test case is done |
#!----------------------------------------------------------------------------------------------------

*** Settings ***
Library     RequestsLibrary
Library     Process
Library     Collections 
Library      ../Library/SensorSimulatorLibrary.py   ${IP_Host_Sensor}     ${Port_Sensor} 
Library      ../Library/StoreTrackerLibrary.py
Library      SSHLibrary

*** Variables ***
${server_endpoint}       http://192.168.31.24:3333
${RPi_client_endpoint}   http://192.168.30.97:4444
${man_in_the_Middle}     http://192.168.31.24:3333
${live_data}  {"frames":[{"events":[{"type":"motion","attributes":{"Event Type":"Enter Line","geometry_name":"sco 1","Event End":"Exit Line"}}]}]} 
${man_in_the_Middle_HOST}        192.168.30.97
${man_in_the_Middle_PORT}             4444
${username}               itab-lia1
${Password}               2024
${Crash_Command}          sudo systemctl restart MITM.service 

*** Keywords ***
#Keyword to retrieve the Store Tracker App from the process library
Retrieve Store Tracker in a separate process from process library                                                          
    [Documentation]    Keyword to retrieve the Store Tracker App from the process library
    Start Process    python    Store_tracker     alias=server    shell=True  

#Keyword to start the Store Tracker App from library    
Store Tracker Start
    [Documentation]    Keyword to start the Store Tracker App from library
    Start Store Tracker 
#Keyword to terminate the Store Tracker App from process library. This also terminates the run function StoreTrackerLibrary.py in library.
Terminate Store Tracker
    [Documentation]    Terminate the Store Tracker App from process library. This also terminates the run function in library.
    Terminate Process    server

#Keyword to send system data between the sensor, man in the middle and store tracker app
Sending System Data
    [Documentation]    Keyword to send data between the sensor, man in the middle and store tracker app
    [Arguments]    ${data}
    Send Data    ${data}

Crash Man in the Middle Server
    [Documentation]    Simulate a crash by sending a request to the crash endpoint.
    [Arguments]    ${RPi_client_endpoint} 
    ${response} =    GET    ${RPi_client_endpoint} /crash

Check Server Running
    [Documentation]    Check if the server is running by sending a GET request.
    [Arguments]    ${endpoint}
    ${response} =    GET    ${endpoint}
    Should Be Equal As Strings    ${response.status_code}    200
    
*** Test Cases ***
Store Tracker start/stop function
    [Documentation]    Test to verify Store Tracker app start and stop functionality
    Retrieve Store Tracker in a separate process from process library  
    Store Tracker Start
    Terminate Store Tracker

Verify Man In The Middle Response From Store Tracker
    [Documentation]    test to verify that the Store_tracker responds to a GET request from man in the middle.
    Start Store Tracker
    Sending System Data   ${live_data}
    ${response} =    GET    ${RPi_client_endpoint}
    Should Be Equal As Strings    ${response.status_code}    200


Verify Man In The Middle Response From SensorSimulator 
    [Documentation]    test to verify that the SensorSimulator responds to a POST request from man in the Middle. 
    Start Store Tracker
    ${response} =    POST    ${RPi_client_endpoint}    ${live_data}
    Should Be Equal As Strings    ${response.status_code}    200
    Log    ${response.content}

Verify Store_tracker Response
    [Documentation]    Verify that the Store_tracker responds to a GET request.
    Start Store Tracker
    ${response} =    GET    ${server_endpoint}
    Should Be Equal As Strings    ${response.status_code}    200

Verify Man in the Middle Restarts if Unexpectedly Terminated
    [Documentation]    Test to verify that the man in the middle successfully restarts after unexpectedly crashing.
    Open Connection    ${man_in_the_Middle_HOST}  
    Login               ${username}  ${Password}
    Execute Command     ${Crash_Command}
    Open Connection    ${man_in_the_Middle_HOST}





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
    Store Tracker Start
    Start Server 
    Sending The Sensor Data      ${live_data}
    ${motion_response} =    POST   ${RPi_client_endpoint}/motion    ${live_data}
    Should Be Equal As Strings    ${motion_response.status_code}    200
    Stop Server

##### this test is just for Omar and Robert #################
#     ${no_motion_response} =    POST    ${RPi_client_endpoint}/motion    json={"event": "no motion"}
#     Should Be Equal As Strings    ${no_motion_response.status_code}    200
#     Should Contain    ${no_motion_response.content}    "No data to send"
##### this test is just for Omar and Robert #################
# Test Zone Names in Events
#     [Documentation]    Test to ensure that motion events correctly include predetermined zone names.
#     @{zones} =    Create List        sco 1    sco 2    sco 3    sco 4    Exit Gate
