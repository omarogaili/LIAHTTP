#in this test i test the Sensor Simulation, if it's sending the data to the RPi and the store tracker APP.
# the keywords:
#  first keyword, i have Start Sensor :  to start the sensor and starting to send the data to the RPi and the store tracker. 
# the second keyword, sending Right Data : send a simple right data to the RPi and the store tracker, motion, one zone, enter line and exit line . this should be pass. 
# the third keyword, sending Wrong Data : i send a wrong data, the varibale Wrong_data, missing the exit line, and that shuold fail, because the sensor need to follow the motion and get the all movements that the object did, whithout 
# missing anything. 
# ***** Variables ****# 
# as i showed previous the first variable is jsut sending a simple right data, have all the expected data from the Sensor. 
# Wrong data is missing the exit line and i use it to fail the test. though no data should be send to the store tracker. 
# as will as the second worng data varibale is sending the sco 6, and in the sensor simulation i dot't have any sco named sco 6, so that should be wrong. 
# the third varibale is moving between the zones, is to test if the objct is moving from the sco 1 to another zone. that should pass becouse the sensor should just fallow the movement and send it to the RPi and Store tracker. 
*** Settings ***
Library  ../Library/SensorSimulatorLibrary.py   192.168.30.97    4444

*** Variables ***
${live_data}  {"frames":[{"events":[{"type":"motion","attributes":{"Event Type":"Enter Line","geometry_name":"sco 1","Event End":"Exit Line"}}]}]} 
${wrong_live_data}   {"frames":[{"events":[{"type":"motion","attributes":{"Event Type":"Enter Line","geometry_name":"sco 1","Event End":}}]}]} 
${wrong_live_data2}  {"frames":[{"events":[{"type":"motion","attributes":{"Event Type":"Enter Line","geometry_name":"sco 1","Event End":"Exit Line","geometry_name":"sco 6"}}]}]}
${live_data_moving_between_the_zones}  {"frames":[{"events":[{"type":"motion","attributes":{"Event Type":"Enter Line","geometry_name":"sco 1","Event End":"Exit Line","geometry_name":"sco 2"}}]}]}

*** Keywords ***
Start Test
    Start Sensor

Sending Right Data
    [Arguments]    ${data}
    Send Data    ${data}
moving between the zones
    [Arguments]    ${data}
    Send Data    ${data}
Sending Wrong Data
    [Arguments]    ${data}
    Run Keyword And Expect Error    *Error sending data*    Send Data    ${data}

*** Test Cases ***
Start Test
    Sending Right Data    ${live_data}

Test wrong Data
    Sending Wrong Data    ${wrong_live_data}

Test wrong Data2
    Sending Wrong Data    ${wrong_live_data2}

Test moving between the zones
    moving between the zones    ${live_data_moving_between_the_zones}