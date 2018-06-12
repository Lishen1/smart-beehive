import sys
sys.path.append('../smart-beehive/')
import time
from sensors.hx711 import *
from actuators.relay import *

WiringProvider.init()

config_path = '/home/user/dev/smart-beehive/app.yml'

weight_sensor = Hx711WeightSensor(
    'WeightSensor', config_path)

fan_relay = RelayModule('FanRelay', config_path)
heater_relay = RelayModule('HeaterRelay', config_path)


try:
    print("Press CTRL+C to exit")
    while True:
        print("hx711 units ", weight_sensor.getWeight())

        fan_relay.switchOff()
        heater_relay.switchOn()

        print('FanRelay', fan_relay.getState())
        print('HeaterRelay', heater_relay.getState())

        time.sleep(0.5)

        fan_relay.switchOn()
        heater_relay.switchOff()

        print('FanRelay', fan_relay.getState())
        print('HeaterRelay', heater_relay.getState())

        time.sleep(0.5)

except KeyboardInterrupt:
    print("hx711 example is over")
