import socketio
import engineio
import time
from datetime import datetime
import threading
import getSerial
from TK4 import Tk4
from KellerPAA import KellerPAA

sio = socketio.Client()

serverInterrupt = False

tk4Port = getSerial.get_autonics()
tk4 = Tk4(tk4Port, False)
keller = KellerPAA(getSerial.get_keller())

allValues: str = ""


@sio.event
def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


@sio.on('Command')
def on_message(data):
    global serverInterrupt, allValues
    print('Message: ', data)
    if data == "ChamberTemperature":
        sio.emit("Result", get_chamber_temperature())
    elif data == "OvenTemperature":
        sio.emit("Result", get_oven_temperature())
    elif data == "KellerTemperature":
        sio.emit("Result", keller.get_temperature())
    elif data == "KellerPressure":
        sio.emit("Result", keller.get_pressure())
    elif data == "All":
        sio.emit("Result", allValues)
    elif "ChamberSet" in data:
        serverInterrupt = True
        value = int(data.split(",")[1])
        tk4.set_value(1, value, 0)
        sio.emit("SetResult", "OK")
        serverInterrupt = False
        print("Chamber set value: {}".format(value))
    elif "OvenSet" in data:
        serverInterrupt = True
        value = int(data.split(",")[1])
        tk4.set_value(2, value, 0)
        sio.emit("SetResult", "OK")
        serverInterrupt = False
        print("Oven set value: {}".format(value))
    else:
        sio.emit("Result", "Error, command not found")


def get_chamber_temperature():
    return tk4.get_temperature(1)


def get_oven_temperature():
    return tk4.get_temperature(2)


def get_chamber_heating_side():
    return tk4.get_heating_side(1)


def get_oven_heating_side():
    return tk4.get_heating_side(2)


def get_chamber_set_value():
    return tk4.get_setvalue(1)


def get_oven_set_value():
    return tk4.get_setvalue(2)


def update():
    global serverInterrupt, allValues
    while True:
        if not serverInterrupt:
            chamberTemperature = get_chamber_temperature()
            time.sleep(0.1)
            ovenTemperature = get_oven_temperature()
            time.sleep(0.1)
            kellerTemperature = keller.get_temperature()
            time.sleep(0.1)
            kellerPressure = keller.get_pressure()
            time.sleep(0.1)
            chamberHeatingSide = get_chamber_heating_side()
            time.sleep(0.1)
            ovenHeatingSide = get_oven_heating_side()
            time.sleep(0.1)
            chamberSetValue = get_chamber_set_value()
            time.sleep(0.1)
            ovenSetValue = get_oven_set_value()
            time.sleep(0.1)
            allValues = "{}, {}, {}, {}, {}, {}, {}, {}".format(chamberTemperature, ovenTemperature,
                                                                chamberHeatingSide, ovenHeatingSide,
                                                                chamberSetValue, ovenSetValue,
                                                                kellerTemperature, kellerPressure)
        time.sleep(1)


# Wait until connection is established with server
while True:
    try:
        x = threading.Thread(target=update)
        x.start()
        sio.connect('http://localhost:3031/', transports=['websocket'])
        sio.wait()
        break
    except:
        print("Connection failed. Retrying...")
