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