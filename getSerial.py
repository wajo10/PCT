import sys
import glob
import serial
import serial.tools.list_ports


def get_ports() -> list:
    totalPorts = list(serial.tools.list_ports.comports())
    ports = []
    for p in totalPorts:
        # print(p.description)
        if "Bluetooth" not in p.description:
            ports.append(p)
    return ports
