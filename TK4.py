import logging

import easymodbus.modbusClient


class Tk4(object):
    def __init__(self, port: str, debug=False, logs=logging.CRITICAL):
        self.port = port
        self.modbus_client = easymodbus.modbusClient.ModbusClient(self.port)
        self.modbus_client.debug = debug
        self.modbus_client.logging_level = logs
        self.modbus_client.connect()

    def start(self, identifier: int):
        """
        Starts Control
        :param identifier:  TK4 Unit Identifier
        """
        self.modbus_client.unitidentifier = identifier
        self.modbus_client.write_single_coil(0, False)
        logging.info("Device #{} Starting".format(identifier))

    def stop(self, identifier: int):
        """
        Stops Control
        :param identifier:  TK4 Unit Identifier
        """
        self.modbus_client.unitidentifier = identifier
        self.modbus_client.write_single_coil(0, True)
        logging.info("Device #{} Stoping".format(identifier))

    def set_unit(self, identifier: int, unit: int):
        """
        Sets Temperature Units for Readings
        :param identifier: TK4 Unit Identifier
        :param unit: 0 for °C / 1 for °F
        """
        self.modbus_client.unitidentifier = identifier

        self.modbus_client.write_single_register(151, unit)

        if self.modbus_client.read_holdingregisters(151, 1)[0] == 0:
            unit = "°C "
        else:
            unit = "°F"
        temp = self.modbus_client.read_inputregisters(1000, 1)[0]
        logging.info("Actual Temperature: {}{} ".format(temp, unit))

    def get_temperature(self, identifier: int) -> float:
        """
        Returns current temperature in given Unit
        :param identifier: TK4 Unit Identifier
        :return: Temperature in °C or °F
        """
        self.modbus_client.unitidentifier = identifier
        temp = self.modbus_client.read_inputregisters(1000, 1)[0]
        logging.info("Temperature device{}: {}".format(identifier, temp))
        return temp

    def get_cooling_side(self, identifier: int) -> float:
        """
        Returns current MV Cooling Side
        :param identifier: TK4 Unit Identifier
        :return: Cooling Side %
        """
        self.modbus_client.unitidentifier = identifier
        cooling_side = self.modbus_client.read_inputregisters(1005, 1)[0] / 10
        logging.info("Cooling Side device{}: {}%".format(identifier, cooling_side))
        return cooling_side

    def get_heating_side(self, identifier: int) -> float:
        """
        Returns current MV Heating Side
        :param identifier: TK4 Unit Identifier
        :return: Heating Side %
        """
        self.modbus_client.unitidentifier = identifier
        heating_side = self.modbus_client.read_inputregisters(1004, 1)[0] / 10
        logging.info("Heating Side device{}: {}%".format(identifier, heating_side))
        return heating_side

    def set_value(self, identifier: int, value: float, unit: int):
        """
        Temperature Set Point for controller
        :param identifier: TK4 Unit Identifier
        :param value: Temperature Value either °C or °F
        :param unit: 0 for °C / 1 for °F
        """
        self.modbus_client.unitidentifier = identifier
        self.modbus_client.write_single_register(151, unit)

        self.modbus_client.write_single_register(57, value)
        logging.info("New Set Value for device{}: {}".format(identifier, value))

    def get_setvalue(self, identifier: int) -> float:
        """
        Get Set Value
        :param identifier: TK4 Unit Identifier
        :return: Temperature Set Value
        """
        self.modbus_client.unitidentifier = identifier
        set_value = self.modbus_client.read_inputregisters(1003, 1)[0]
        logging.info("Set Value for device{}: {}".format(identifier, set_value))
        return set_value

    def get_proportional(self, identifier: int) -> float:
        """
        Returns Heating Proportional value
        :param identifier: TK4 Unit Identifier
        :return: Heating Proportional Band either in °C or °F
        """
        self.modbus_client.unitidentifier = identifier
        proportional = self.modbus_client.read_holdingregisters(101, 1)[0] / 10
        logging.info("Proportional band:{} ".format(proportional))
        return proportional

    def set_proportional(self, identifier: int, value: float):
        """
        Sets Heating Proportional value
        :param identifier: TK4 Unit Identifier
        :param value: Proportional Value either in °C or °F
        """
        self.modbus_client.unitidentifier = identifier
        self.modbus_client.write_single_register(101, value * 10)
        logging.info("New Proportional: {}".format(value))

    def get_integral(self, identifier: int) -> float:
        """
        Returns Heating Integral Time
        :param identifier: TK4 Unit Identifier
        :return: Heating Integral Time in Sec.
        """

        self.modbus_client.unitidentifier = identifier
        integral = self.modbus_client.read_holdingregisters(103, 1)[0]
        logging.info("Heating Integral Time: {}".format(integral))
        return integral

    def set_integral(self, identifier: int, value: float):
        """
        Sets Heating Integral Time
        :param identifier: TK4 Unit Identifier
        :param value: Time in Sec
        """
        self.modbus_client.unitidentifier = identifier
        self.modbus_client.write_single_register(103, value)
        logging.info("New Integral: {}".format(value))

    def get_derivative(self, identifier: int) -> float:
        """
        Returns Heating Derivative Time
        :param identifier: TK4 Unit Identifier
        :return: Heating Derivative Time in Sec.
        """
        self.modbus_client.unitidentifier = identifier
        derivative = self.modbus_client.read_holdingregisters(105, 1)[0]
        logging.info("Heating Integral Time: {}".format(derivative))
        return derivative

    def set_derivative(self, identifier: int, value: float):
        """
        Sets Heating Derivative Time
        :param identifier: TK4 Unit Identifier
        :param value: Time in Sec
        """
        self.modbus_client.unitidentifier = identifier
        self.modbus_client.write_single_register(105, value)
        logging.info("New derivative: {}".format(value))
