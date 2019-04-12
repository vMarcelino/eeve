import travel_backpack


class WinLowLevelHook(metaclass=travel_backpack.Singleton):
    def __init__(self, keyboard_callback, mouse_callback):
        import collections
        self.keyboard_callback = keyboard_callback
        self.mouse_callback = mouse_callback
        self.KeyboardEvent = collections.namedtuple('KeyboardEvent', ['event_type', 'key_code', 'scan_code', 'alt_pressed', 'time'])
        self.MouseEvent = collections.namedtuple('MouseEvent', ['event_type', 'point', 'wheel_direction', 'injection', 'time'])

        self.hook_id_keyboard = None
        self.hook_id_mouse = None

    def start(self, asynchronous=True):
        if asynchronous:
            print('async hook')
            import threading
            threading.Thread(target=self.start, kwargs={'asynchronous': False}).start()
            return

        print('starting hook')
        import win32con
        keyboard_event_types = {
            win32con.WM_KEYDOWN: 'key down',
            win32con.WM_KEYUP: 'key up',
            0x104: 'key down',  # WM_SYSKEYDOWN, used for Alt key.
            0x105: 'key up',  # WM_SYSKEYUP, used for Alt key.
        }

        # WM_LBUTTONDOWN, WM_LBUTTONUP, WM_MOUSEMOVE, WM_MOUSEWHEEL, WM_MOUSEHWHEEL, WM_RBUTTONDOWN, or WM_RBUTTONUP.
        mouse_event_types = {
            win32con.WM_RBUTTONDOWN: 'RMB down',
            win32con.WM_RBUTTONUP: 'RMB up',
            win32con.WM_LBUTTONDOWN: 'LMB down',
            win32con.WM_LBUTTONUP: 'LMB up',
            0x0207: 'MMB down',
            0x0208: 'MMB up',
            win32con.WM_MOUSEWHEEL: 'Wheel',
            0x020E: 'Horizontal Wheel',  # win32con.WM_MOUSEHWHEEL
            win32con.WM_MOUSEMOVE: 'mouse move'
        }

        def low_level_keyboard_handler(nCode, wParam, lParam):
            event = (nCode,
                     self.KeyboardEvent(
                         event_type=keyboard_event_types[wParam],
                         key_code=lParam[0],
                         scan_code=lParam[1],
                         alt_pressed=lParam[2] == 32,
                         time=lParam[3]))

            # Be a good neighbor and call the next hook.
            if self.keyboard_callback(event):
                return ctypes.windll.user32.CallNextHookEx(self.hook_id_keyboard, nCode, wParam, lParam)
            else:
                print("#")
                return 1

        def low_level_mouse_handler(nCode, wParam, lParam):
            event = (nCode,
                     self.MouseEvent(
                         event_type=mouse_event_types.get(wParam, f'unknown ({hex(wParam)})'),
                         point=lParam[0],
                         wheel_direction=lParam[1],
                         injection=lParam[2],
                         time=lParam[3]))

            if self.mouse_callback(event):
                # Be a good neighbor and call the next hook.
                return ctypes.windll.user32.CallNextHookEx(self.hook_id_mouse, nCode, wParam, lParam)
            else:
                return 1

        import ctypes
        CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))
        # Convert the Python handler into C pointer.
        pointer_keyboard = CMPFUNC(low_level_keyboard_handler)
        pointer_mouse = CMPFUNC(low_level_mouse_handler)

        import win32api
        # Hook both key up and key down events for common keys (non-system).
        try:
            wh_keyboard_lo_level = win32con.WH_KEYBOARD_LL
            wh_mouse_low_level = win32con.WH_MOUSE_LL
            p_keyoard = pointer_keyboard
            p_mouse = pointer_mouse
            module_handle = win32api.GetModuleHandle(None)
            module_handle = 0
            self.hook_id_keyboard = ctypes.windll.user32.SetWindowsHookExA(wh_keyboard_lo_level, p_keyoard, module_handle, 0)
            self.hook_id_mouse = ctypes.windll.user32.SetWindowsHookExA(wh_mouse_low_level, p_mouse, module_handle, 0)

        except Exception as ex:
            print(ex)

        # Register to remove the hook when the interpreter exits.
        # Unfortunately a
        # try/finally block doesn't seem to work here.
        import atexit
        atexit.register(ctypes.windll.user32.UnhookWindowsHookEx, self.hook_id_keyboard)
        atexit.register(ctypes.windll.user32.UnhookWindowsHookEx, self.hook_id_mouse)

        while True:
            import win32gui
            #peek_result, msg = win32gui.PeekMessage(None, 0, 0, 1)
            result, msg = win32gui.GetMessage(None, 0, 0)
            print('got msg:', msg)
            win32gui.TranslateMessage(msg)
            #print('translated')
            win32gui.DispatchMessage(msg)
            #print('sent')
            #sleep(0.5)
            pass


from uuid import uuid4


class KeyHookWrapper(metaclass=travel_backpack.Singleton):
    def __init__(self):
        self.keyboard_callbacks = dict()
        self.mouse_callbacks = dict()

        def keyboard_callback(key_name):
            for cb in self.keyboard_callbacks.values():
                cb(key_name=key_name)
            return True

        def mouse_hook_callback(info):
            nCode, event = info
            if event.event_type == 'LMB down':
                for cb in self.mouse_callbacks.values():
                    cb(key_name=event.event_type,
                       point=event.point,
                       wheel_direction=event.wheel_direction,
                       injection=event.injection,
                       time=event.time)
            return True

        from win_key_hook.input_parser import InputParser
        parser = InputParser(key_down_callback=keyboard_callback, key_up_callback=None)
        hook = WinLowLevelHook(parser.process_keyboard_event, mouse_hook_callback)

        print('Starting input hook')
        hook.start()

    def add_keyboard_callback(self, callback):
        uuid = uuid4()
        self.keyboard_callbacks[uuid] = callback
        return uuid

    def remove_keyboard_callback(self, uuid):
        del self.keyboard_callbacks[uuid]

    def add_mouse_callback(self, callback):
        uuid = uuid4()
        self.mouse_callbacks[uuid] = callback
        return uuid

    def remove_mouse_callback(self, uuid):
        del self.mouse_callbacks[uuid]


class RegisterKeyDown:
    def __init__(self, action):
        self.uuid = KeyHookWrapper().add_keyboard_callback(action)

    def unregister(self):
        KeyHookWrapper().remove_keyboard_callback(self.uuid)


class RegisterMouseDown:
    def __init__(self, action):
        self.uuid = KeyHookWrapper().add_mouse_callback(action)

    def unregister(self):
        KeyHookWrapper().remove_mouse_callback(self.uuid)


triggers = {'key down': RegisterKeyDown, 'mouse down': RegisterMouseDown}

if __name__ == '__main__':
    import sys
    Request().run(*sys.argv[1:])
