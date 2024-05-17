*** Settings ***
Library  SensorSimulator.py       ${HOST}  ${PORT} 
Library   Process

*** Variables ***
${HOST}  192.168.30.97
${PORT}  4444

*** Test Cases ***
Test Client Simulator
    [Documentation]  Test to start the Client Simulator and verify its behavior
    Start Client Simulator 

*** Keywords ***
Start Client Simulator
    ClientSimulator.send_data    omar
