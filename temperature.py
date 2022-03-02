from TK4 import Tk4
import logging

tk4 = Tk4("COM18", False, logging.CRITICAL)

print("Device 1:{}°C Device 2:{}°C".format(tk4.get_temperature(1), tk4.get_temperature(2)))
print("Heating Side: {}".format(tk4.get_heating_side(2)))
print("Set Value: {}".format(tk4.get_setvalue(2)))
print("Proportional:{}".format(tk4.get_proportional(2)))
print("Integral: {}".format(tk4.get_integral(2)))
print("Derivative: {}".format(tk4.get_derivative(2)))