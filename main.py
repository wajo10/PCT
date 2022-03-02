import time
import serial
import struct
import csv


def sensor_float(Rx):
    B = []
    sz = len(Rx)
    B.append(Rx[sz - 6])
    B.append(Rx[sz - 5])
    B.append(Rx[sz - 4])
    B.append(Rx[sz - 3])

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


# sensor_float([1, 3, 0, 2, 0, 2, 101, 203, 1, 3, 4, 63, 101, 226, 208, 175, 4])
# print(sensor_float([1, 3, 0, 8, 0, 2, 69, 201, 1, 3, 4, 65, 198, 7, 0, 170, 146]))

ser = serial.Serial('COM25', 9600, timeout=0.5)
pres = [1, 3, 0, 2, 0, 2, 101, 203]
temp = [1, 3, 0, 8, 0, 2, 69, 201]
with open('data.csv', 'w+') as f:
    writer = csv.writer(f)

    writer.writerow(["Pressure", "Temperature"])
    cont = 0
    while True:
        # Medicion Presion
        ser.write(struct.pack('BBBBBBBB', *pres))
        try:
            rx = struct.unpack('%dB' % 17, ser.readline())
            pressure = sensor_float(rx)
            # Medicion Temperatura
            ser.write(struct.pack('BBBBBBBB', *temp))
            rx = struct.unpack('%dB' % 17, ser.readline())
            temperature = sensor_float(rx)

            writer.writerow([str(pressure), str(temperature)])
            print("Pressure:", pressure, "bar, Temperature: ", temperature, "°C")
            cont += 1
        except:
            print("Error Reading")


# ser.close()
