import socketio
import engineio
import time
from datetime import datetime
import threading
import getSerial
from TK4 import Tk4
from KellerPAA import KellerPAA
from Writer import Writer
import datetime

sio = socketio.Client()

serverInterrupt = False

tk4Port = getSerial.get_autonics()
tk4 = Tk4(tk4Port, False)
keller = KellerPAA(getSerial.get_keller())

allValues: str = ""
logging = logging_aux = False


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
    elif data == "StartLogging":
        start_logging()
        sio.emit("StartResult", "OK")
    elif data == "StopLogging":
        stop_logging()
        sio.emit("StopResult", "OK")

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
    global serverInterrupt, allValues, logging, logging_aux
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
            allValues = '{{"ChamberTemp":{}, "OvenTemp":{}, "ChamberHeating":{}, "OvenHeating":{}, "ChamberSetValue":{}, ' \
                        '"OvenSetValue":{}, "KellerTemp":{}, "KellerPress":{}}}'.format(
                chamberTemperature, ovenTemperature,
                chamberHeatingSide, ovenHeatingSide,
                chamberSetValue, ovenSetValue,
                kellerTemperature, kellerPressure)
            if logging:
                if logging_aux:
                    header = ["Timestamp", "Chamber Temperature", "Oven Temperature", "Chamber Heating Side",
                              "Oven Heating Side",
                              "Chamber Set Value", "Oven Set Value", "Chamber Proportional", "Oven Proportional",
                              "Chamber Integral", "Oven Integral", "Chamber Derivative", "Oven Derivative",
                              "Keller Temperature", "Keller Pressure"]
                    writer = Writer('register.csv', header)
                    logging_aux = False
                values = [datetime.datetime.now(), chamberTemperature, ovenTemperature,
                          chamberHeatingSide, ovenHeatingSide, chamberSetValue, ovenSetValue, tk4.get_proportional(1),
                          tk4.get_proportional(2), tk4.get_integral(1), tk4.get_integral(2), tk4.get_derivative(1),
                          tk4.get_derivative(2), kellerTemperature, kellerPressure]
                writer.write_row(values)
                print(values)

        time.sleep(1)

def start_logging():
    global logging, logging_aux

    #clear register.csv
    with open('register.csv', 'w') as f:
        f.write('')
        f.close()
    logging = True
    logging_aux = True

def stop_logging():
    global logging
    logging = False




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
