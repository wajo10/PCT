import sys
import glob
import serial
import serial.tools.list_ports


def get_ports() -> list:
    totalPorts = list(serial.tools.list_ports.comports())
    ports = []
    for p in totalPorts:
        if "Bluetooth" not in p.description:
            ports.append(p)
            print(p.name)
    return ports


def get_autonics() -> str:
    totalPorts = list(serial.tools.list_ports.comports())
    for p in totalPorts:
        if p.serial_number == "A907ZIHUA":
            return p.device
    return ''

def get_keller() -> str:
    totalPorts = list(serial.tools.list_ports.comports())
    for p in totalPorts:
        if p.serial_number == "5":
            return p.device
    return ''
