import wiringpi as wi
from enum import Enum
from collections import namedtuple

class PortType(Enum):
    IN = wi.INPUT
    OUT = wi.OUTPUT

Port = namedtuple('Port', [
    'index',
    'type',
])


class WiringProvider:
    """
    Arbitr for centralized providing access to wiringOP library
    """
    ports = {}
    inited = False

    def __init__(self):
        pass

    @staticmethod
    def getPort(owner_name, port_type, port_idx):
        
        if not WiringProvider.inited:
            WiringProvider.init()

        if (owner_name, port_idx) in WiringProvider.ports.keys():
            raise KeyError(f'port {port_idx} type {port_type} already owned by {owner_name}')

        port = Port(port_idx, port_type)
        WiringProvider.ports[(owner_name, port_idx)] = port
        return port

    @staticmethod
    def init():
        if not WiringProvider.inited:
            res = wi.wiringPiSetup()
            if res != 0:
                raise RuntimeError(f'wiringPiSetup returned {res}')
            WiringProvider.inited = True
