class InputParser:
    def __init__(self, key_down_callback=None, key_up_callback=None, keys_down=None):
        if keys_down is None:
            self.keys_down = set()
        else:
            self.keys_down = keys_down

        self.key_down_callback = key_down_callback
        self.key_up_callback = key_up_callback

    def process_keyboard_event(self, event):
        # print(event)
        nCode, e = event
        key_code = e.key_code & 0xFFFFFFFF
        key_code_special = 0
        key_name = hex(e.key_code)[2:]
        key_code_special = int((e.key_code & 0xFF00000000) / 0x100000000)

        special = False
        import win_key_hook.key_map as key_map
        try:
            key_name = key_map.key_code_map[key_code]
        except KeyError:
            try:
                key_name = key_map.key_code_map[e.key_code & 0xFFFFFFFFF]
            except KeyError:
                try:
                    key_name = key_map.key_code_special_map[key_code_special]
                    special = True
                except KeyError:
                    pass

        if e.event_type == 'key down':
            return self.on_key_down(key_name, special)
        else:
            return self.on_key_up(key_name)

    def on_key_down(self, key_name, is_special_key):
        print(key_name, end='', flush=True)
        if key_name == 'F12':
            return False

        self.keys_down.add(key_name)

        if 'F2' in self.keys_down and 'LControlKey' in self.keys_down:
            import user_interface
            if user_interface.main_window.IsVisible:
                user_interface.hide_window()
            else:
                user_interface.show_window()

        if self.key_down_callback is not None:
            return self.key_down_callback(key_name)

        return True

    def on_key_up(self, key_name):
        if key_name == 'F12':
            exit()

        try:
            self.keys_down.remove(key_name)
        except KeyError as ke:
            print('\nkey error:', ke)
        except Exception as ex:
            import exception_handler
            exception_handler.print_traceback(ex)

        if self.key_up_callback is not None:
            return self.key_up_callback(key_name)

        return True