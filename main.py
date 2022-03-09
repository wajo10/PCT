from TK4 import Tk4
from KellerPAA import KellerPAA
import logging

tk4 = Tk4("COM18", False, logging.CRITICAL)
keller = KellerPAA("COM20")

print("Device 1:{}°C Device 2:{}°C".format(tk4.get_temperature(1), tk4.get_temperature(2)))
print("Heating Side: {}".format(tk4.get_heating_side(1)))
print("Set Value: {}".format(tk4.get_setvalue(1)))
print("Proportional:{}".format(tk4.get_proportional(1)))
print("Integral: {}".format(tk4.get_integral(1)))
print("Derivative: {}".format(tk4.get_derivative(1)))

print("Keller Temperature: {}°C, Keller Pressure: {} kPa".format(keller.get_temperature(), keller.get_pressure()*100))