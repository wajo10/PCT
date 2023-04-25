from TK4 import Tk4
import logging

tk4 = Tk4("COM18", False, logging.CRITICAL)

print("Device 1:{}°C Device 2:{}°C".format(tk4.get_temperature(1), tk4.get_temperature(2)))
print("Heating Side: {}".format(tk4.get_heating_side(1)))
print("Set Value: {}".format(tk4.get_setvalue(1)))
print("Proportional:{}".format(tk4.get_proportional(1)))
print("Integral: {}".format(tk4.get_integral(1)))
print("Derivative: {}".format(tk4.get_derivative(1)))
