*** Settings ***
Library  SensorSimulatorLibrary.py  192.168.30.97    4444

*** Variables ***
${live_data}

*** Keywords ***
Start Test
    Start Sensor
Sending Test
    Send Data      {"frames":[{"events":[{"type":"motion","attributes":{"Event Type":"Enter Line","geometry_name":"sco 1","Event End":"Exit Line"}}]}]}
# Stop Test
#     Stop Run
Cutom Data
    Send Custom Data    ${live_data}

*** Test Cases ***
Start Test
    Start Sensor
