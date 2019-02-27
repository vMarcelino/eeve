from travel_backpack import log_info
import win32con
import win32api
import win32gui
import time
from ctypes import POINTER, windll, Structure, cast, CFUNCTYPE, c_int, c_uint, c_void_p, c_bool
from comtypes import GUID
from ctypes.wintypes import HANDLE, DWORD
from datetime import datetime as dt
now = dt.now

h_log_info = log_info
log_info = lambda info: h_log_info(info, file='System.log')

PBT_POWERSETTINGCHANGE = 0x8013

display_on_callbacks = dict()
display_off_callbacks = dict()
display_dim_callbacks = dict()
session_end_callbacks = dict()
sys_suspend_callbacks = dict()


def display_change(data):
    mapping = {0: 'off', 1: 'on', 2: 'dimmed'}
    status = mapping[data]
    if status == 'on':
        for c in display_on_callbacks.values():
            print('fon')
            c()
    elif status == 'off':
        for c in display_off_callbacks.values():
            print('foff')
            c()
    elif status == 'dimmed':
        for c in display_dim_callbacks.values():
            print('fdim')
            c()

    return "Display " + status


power_settings = {
    'SYSTEM_AWAYMODE': {
        'GUID': '{98A7F580-01F7-48AA-9C0F-44352C29E5C0}',
        'Data': {
            0: 'Exiting away mode',
            1: 'Entering away mode'
        }
    },
    'CONSOLE_DISPLAY_STATE': {
        'GUID': '{6FE69556-704A-47A0-8F24-C28D936FDA47}',
        'Data': display_change
    },
    'ACDC_POWER_SOURCE': {
        'GUID': '{5D3E9A59-E9D5-4B00-A6BD-FF34FF516548}',
        'Data': {
            0: 'AC power',
            1: 'DC power (batteries)',
            2: 'Short term power source (UPS)'
        }
    },
    'BATTERY_PERCENTAGE_REMAINING': {
        'GUID': '{A7AD8041-B45A-4CAE-87A3-EECBB468A9E1}',
        'Data': lambda batt: f'Battery remaining: {batt}'
    }
}

GUID_to_name = {v['GUID']: k for k, v in power_settings.items()}


def process_power_broadcast(lparam):
    settings = cast(lparam, POINTER(POWERBROADCAST_SETTING)).contents

    power_setting_GUID = str(settings.PowerSetting)
    data_length = settings.DataLength
    data = settings.Data

    data_info = power_settings.get(GUID_to_name.get(power_setting_GUID)).get('Data')
    if data_info is None:
        log_info(f'Power setting changed but GUID is unknown: {power_setting_GUID}')

    elif callable(data_info):
        log_info(data_info(data))
    else:
        log_info(data_info.get(data, f'Unknown Data: {hex(data)}({data})'))


def system_suspend(x):
    for c in sys_suspend_callbacks.values():
        print('fssus')
        c()
    log_info('System suspend')


power_broadcast_wParams = {
    win32con.PBT_APMPOWERSTATUSCHANGE: lambda x: log_info('Power status has changed'),
    win32con.PBT_APMRESUMEAUTOMATIC: lambda x: log_info('System resume'),
    win32con.PBT_APMRESUMESUSPEND: lambda x: log_info('System resume by user input'),
    win32con.PBT_APMSUSPEND: system_suspend,
    PBT_POWERSETTINGCHANGE: process_power_broadcast
}

end_session_lParams = {
    0x00000000: 'Shutdown or Restart',
    0x00000001: 'Using file that must be replaced, system being serviced or resourses exausted',
    0x40000000: 'Force shutdown',
    0x80000000: 'User logging off'
}


class POWERBROADCAST_SETTING(Structure):
    _fields_ = [("PowerSetting", GUID), ("DataLength", DWORD), ("Data", DWORD)]


def wndproc(hwnd, msg, wparam, lparam):
    if msg == win32con.WM_POWERBROADCAST:
        power_broadcast_wParams.get(wparam, lambda x: log_info(f'Unknown wParam for WM_POWERBROADCAST ({wparam})'))(lparam)
        return True

    elif msg == win32con.WM_QUERYENDSESSION:
        for c in session_end_callbacks.values():
            print('fsend')
            c()
        for k, v in end_session_lParams.items():
            if lparam & k:
                log_info(v)
        #return False # to cancel shutdown
        return True

    elif msg == win32con.WM_ENDSESSION:
        for k, v in end_session_lParams.items():
            if lparam & k:
                log_info(v)
        return 0

    else:
        log_info(f"wndproc: {msg}\nw: {hex(wparam)}\nl: {hex(lparam)}")


running = False


def run():
    global running
    if running:
        return
    running = True
    log_info("*** STARTING ***")
    running = True
    hinst = win32api.GetModuleHandle(None)
    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = hinst
    wndclass.lpszClassName = "testWindowClass"
    CMPFUNC = CFUNCTYPE(c_bool, c_int, c_uint, c_uint, c_void_p)
    wndproc_pointer = CMPFUNC(wndproc)
    messageMap = {
        win32con.WM_POWERBROADCAST: wndproc_pointer,
        win32con.WM_QUERYENDSESSION: wndproc,
        win32con.WM_ENDSESSION: wndproc,
        win32con.WM_SYSCOMMAND: wndproc,
        win32con.WM_DESTROY: wndproc,
        win32con.WM_CLOSE: wndproc,
        win32con.WM_QUIT: wndproc
    }

    wndclass.lpfnWndProc = messageMap

    try:
        myWindowClass = win32gui.RegisterClass(wndclass)
        hwnd = win32gui.CreateWindowEx(win32con.WS_EX_LEFT, myWindowClass, "testMsgWindow", 0, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                       0, 0, hinst, None)
    except Exception as e:
        log_info("Exception: %s" % str(e))

    if hwnd is None:
        log_info("hwnd is none!")
    else:
        log_info("hwnd: %s" % hwnd)

    register_function = windll.user32.RegisterPowerSettingNotification
    hwnd_pointer = HANDLE(hwnd)
    for name, power_setting_info in power_settings.items():
        result = register_function(hwnd_pointer, GUID(power_setting_info['GUID']), DWORD(0))
        print('registering', name)
        #print('result:', hex(result))
        #print('lastError:', win32api.GetLastError())
        #print()

    print('\nEntering loop')
    while True:
        win32gui.PumpWaitingMessages()
        time.sleep(1)
        #print('.', end='', flush=True)


if __name__ == "__main__":
    run()


def thread_run():

    import travel_backpack
    travel_backpack.threadpool(run)()

    return
    global running
    if not running:
        running = True
        import travel_backpack
        travel_backpack.threadpool(run)()


class Display:
    def __init__(self, action, status):
        from uuid import uuid4
        self.uuid = uuid4()
        self.mappings = {'on': display_on_callbacks, 'off': display_off_callbacks, 'dimmed': display_dim_callbacks}
        self.status = status
        #print(action)
        self.mappings[self.status][self.uuid] = action
        thread_run()

    def unregister(self):
        del self.mappings[self.status][self.uuid]


class SessionEnd:
    def __init__(self, action):
        from uuid import uuid4
        self.uuid = uuid4()
        session_end_callbacks[self.uuid] = action

        thread_run()

    def unregister(self):
        del session_end_callbacks[self.uuid]


class SystemSuspend:
    def __init__(self, action):
        from uuid import uuid4
        self.uuid = uuid4()
        sys_suspend_callbacks[self.uuid] = action

        thread_run()

    def unregister(self):
        del sys_suspend_callbacks[self.uuid]


triggers = {'display': Display, 'session end': SessionEnd, 'system suspend': SystemSuspend}
