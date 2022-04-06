import logging
import sched
import time
import datetime

from KellerPAA import KellerPAA
from TK4 import Tk4
from Writer import Writer

tk4 = Tk4("COM18", False, logging.CRITICAL)
keller = KellerPAA("COM20")

print("Device 1:{}°C Device 2:{}°C".format(tk4.get_temperature(1), tk4.get_temperature(2)))
print("Heating Side: {}".format(tk4.get_heating_side(1)))
print("Set Value: {}".format(tk4.get_setvalue(1)))
print("Proportional:{}".format(tk4.get_proportional(1)))
print("Integral: {}".format(tk4.get_integral(1)))
print("Derivative: {}".format(tk4.get_derivative(1)))

print("Keller Temperature: {}°C, Keller Pressure: {} kPa".format(keller.get_temperature(), keller.get_pressure()))

header = ["Timestamp", "Device1 Temperature", "Device2 Temperature", "Device1 Heating Side",
          "Device2 Heating Side",
          "Device1 Set Value", "Device2 Set Value", "Device1 Proportional", "Device2 Proportional",
          "Device1 Integral", "Device2 Integral", "Device1 Derivative", "Device2 Derivative",
          "Keller Temperature", "Keller Pressure"]
writer = Writer('register.csv', header)


def save_data(sc):
    values = [datetime.datetime.now(), tk4.get_temperature(1), tk4.get_temperature(2), tk4.get_heating_side(1),
              tk4.get_heating_side(2), tk4.get_setvalue(1), tk4.get_setvalue(2), tk4.get_proportional(1),
              tk4.get_proportional(2), tk4.get_integral(1), tk4.get_integral(2), tk4.get_derivative(1),
              tk4.get_derivative(2), keller.get_temperature(), keller.get_pressure()]
    writer.write_row(values)
    print(values)
    s.enter(10, 1, save_data, (sc,))
    s.run()


s = sched.scheduler(time.time, time.sleep)
s.enter(10, 1, save_data, (s,))
s.run()