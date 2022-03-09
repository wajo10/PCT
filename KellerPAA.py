import time
import serial
import struct


def sensor_float(rx):
    B = []
    sz = len(rx)
    B.append(rx[sz - 6])
    B.append(rx[sz - 5])
    B.append(rx[sz - 4])
    B.append(rx[sz - 3])

    v_res = ""
    for i in range(len(B)):
        v_bit = bin(B[i]).replace("0b", "")
        if len(v_bit) < 8:
            for j in range(8 - len(v_bit)):
                v_bit = "0" + v_bit
        v_res = v_res + v_bit
    s_mnt = int(v_res[0], 2)
    e = v_res[1:9]
    E = int(e, 2)
    m = v_res[9:32]
    M = int(m, 2)
    if s_mnt == 0:
        val = (1 + M / 8388608) * 2 ** (E - 127)
    else:
        val = -(1 + M / 8388608) * 2 ** (E - 127)
    return val


class KellerPAA(object):
    def __init__(self, port):
        self.pressure = [1, 3, 0, 2, 0, 2, 101, 203]
        self.temperature = [1, 3, 0, 8, 0, 2, 69, 201]
        self.port = port
        self.serial = serial.Serial(self.port, 9600, timeout=0.5)

    def get_temperature(self) -> float:
        self.serial.write(struct.pack('BBBBBBBB', *self.temperature))
        rx = struct.unpack('%dB' % 17, self.serial.readline())
        return sensor_float(rx)

    def get_pressure(self) -> float:
        self.serial.write(struct.pack('BBBBBBBB', *self.pressure))
        rx = struct.unpack('%dB' % 17, self.serial.readline())
        return sensor_float(rx)
