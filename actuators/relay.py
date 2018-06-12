from drivers.wiring import *
import yaml
from enum import Enum


class RelayModule:
    """
    Wraps functionality around wiringOP library for usual relay module sensor support
    """

    class State(Enum):
        ON = 1
        OFF = 0

    def __init__(self, name, config_path):
        self.name = name
        self.pin = None
        self.state = RelayModule.State.OFF

        cfg = yaml.load(open(config_path, 'r'))

        actuators_cfg = cfg['actuators']
        my_cfg = actuators_cfg[name]
        pin = my_cfg['pin']

        self.__setPin(pin)

    def switchOn(self):
        wi.digitalWrite(self.pin, wi.HIGH)
        self.state = RelayModule.State.ON

    def switchOff(self):
        wi.digitalWrite(self.pin, wi.LOW)
        self.state = RelayModule.State.OFF

    def getState(self):
        return self.state

    def __del__(self):
        self.switchOff()

    def __setPin(self, pin):
        WiringProvider.getPort(self.name, PortType.OUT, pin)
        wi.pinMode(pin, wi.OUTPUT)
        self.pin = pin
