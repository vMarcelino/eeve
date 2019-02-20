from pyHS100 import Discover
import travel_backpack
import time


class SmartDeviceContainer:
    def __init__(self, dev):
        self.device = dev
        self.hw_id = self.device.hw_info['hwId']
        self.alias = self.device.alias

    def __hash__(self):
        h = hash(self.hw_id)
        #print('hash:', h)
        return h

    def __eq__(self, other):
        return self.hw_id == other.hw_id

    def __repr__(self):
        alias = self.alias + ' (offline)'
        try:
            alias = self.device.alias
        except:
            pass
        return alias


def repr(self):
    return self.alias


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class Discoverer(metaclass=Singleton):
    def __init__(self):
        print('inited')
        self.timeout = 1
        self.time_between_pings = 0

        self.single_connect_event = []
        self.single_disconnect_event = []

        self.multi_connect_event = []
        self.multi_disconnect_event = []

        self.discoverer_thread = self.discoverer()

    def set_params(self, timeout, time_between_pings):
        self.timeout = timeout
        self.time_between_pings = time_between_pings

    @travel_backpack.threadpool
    def discoverer(self):
        current_device_set = set()
        while True:
            #print('\nloop start')
            new_device_set = set()
            for ip, dev in Discover.discover(timeout=self.timeout).items():
                try:
                    dev = SmartDeviceContainer(dev)
                    new_device_set.add(dev)
                except:
                    pass

            new_devices = new_device_set - current_device_set
            #print('new_devices:'.ljust(18), (new_devices) or '-')
            for e in self.multi_connect_event:
                e(device_list=[d.device for d in new_devices])
            for dev in new_devices:
                for e in self.single_connect_event:
                    e(device=dev.device)

            offline_devices = current_device_set - new_device_set
            #print('offline devices:'.ljust(18), (offline_devices) or '-')
            for e in self.multi_disconnect_event:
                e(device_list=[d.device for d in offline_devices])
            for dev in offline_devices:
                for e in self.single_disconnect_event:
                    e(device=dev.device)

            #print('noch:'.ljust(18), (new_device_set & current_device_set) or '-')
            current_device_set = new_device_set

            time.sleep(self.time_between_pings)


def register_trigger(action, trigger_status, mult='single', timeout=3, time_between_pings=3):
    d = Discoverer()
    if trigger_status == 'connect':
        if mult == 'single':
            d.single_connect_event.append(action)
        elif mult == 'multi':
            d.multi_connect_event.append(action)
    elif trigger_status == 'disconnect':
        if mult == 'single':
            d.single_disconnect_event.append(action)
        elif mult == 'multi':
            d.multi_disconnect_event.append(action)


def set_device_property(device, brightness=None, temperature=None, is_on=None):
    if brightness is not None:
        device.brightness = brightness
    if temperature is not None:
        device.color_temp = temperature
    if is_on is not None:
        if is_on:
            device.turn_on()
        else:
            device.turn_off()


actions = {'set TP-Link device property': {'run': set_device_property}}
triggers = {'TP-Link device': register_trigger}

if __name__ == "__main__":

    def a(*args, **kwargs):
        print('==>', *args, **kwargs)

    def b(*args, **kwargs):
        print('<==', *args, **kwargs)

    register_trigger(a, 'connect')

    register_trigger(b, 'disconnect')
