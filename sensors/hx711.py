from drivers.wiring import *
import yaml

class Hx711WeightSensor:
    """
    Wraps functionality around wiringOP library for hx7111 weight sensor support
    """
    instId = 0

    def __init__(self, name, config_path):
        self.name = name
        self.measure_times = 10
        self.instId = Hx711WeightSensor.instId

        cfg = yaml.load(open(config_path, 'r'))

        sensors_cfg = cfg['sensors']
        my_cfg = sensors_cfg[name]

        clockPin = my_cfg['clockPin']
        dataPin = my_cfg['dataPin']
        offset = my_cfg['offset']
        scale = my_cfg['scale']

        self.__setPins(clockPin, dataPin)
        res = wi.hx711Setup(self.clockPin, self.dataPin, 1, self.instId)
        if res != 0:
            raise RuntimeError(
                f'Hx711WeightSensor with name {self.name} and instId {self.instId} returned {res} from hx711Setup()')

        wi.hx711PowerUp(self.instId)
        wi.hx711Tare(self.measure_times, self.instId)
        wi.hx711SetScale(scale, self.instId,)
        wi.hx711SetOffset(offset, self.instId)
        wi.hx711SetGain(128, self.instId)

        Hx711WeightSensor.instId += 1

    def getWeight(self):
        return wi.hx711GetUnits(self.measure_times, self.instId)

    def __del__(self):
        wi.hx711PowerDown(self.instId)

    def __setPins(self, clockPin, dataPin):
        WiringProvider.getPort(self.name, PortType.OUT, clockPin)
        WiringProvider.getPort(self.name, PortType.IN, dataPin)
        self.clockPin = clockPin
        self.dataPin = dataPin
