import win32api, time, win32con
from typing import Union, Dict, List
#Giant dictonary to hold key name and VK value
VK_CODE = {
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'alt': 0x12,
    'pause': 0x13,
    'caps_lock': 0x14,
    'esc': 0x1B,
    'spacebar': 0x20,
    'page_up': 0x21,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print_screen': 0x2C,
    'ins': 0x2D,
    'del': 0x2E,
    'help': 0x2F,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'numpad_0': 0x60,
    'numpad_1': 0x61,
    'numpad_2': 0x62,
    'numpad_3': 0x63,
    'numpad_4': 0x64,
    'numpad_5': 0x65,
    'numpad_6': 0x66,
    'numpad_7': 0x67,
    'numpad_8': 0x68,
    'numpad_9': 0x69,
    'multiply_key': 0x6A,
    'add_key': 0x6B,
    'separator_key': 0x6C,
    'subtract_key': 0x6D,
    'decimal_key': 0x6E,
    'divide_key': 0x6F,
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    'F13': 0x7C,
    'F14': 0x7D,
    'F15': 0x7E,
    'F16': 0x7F,
    'F17': 0x80,
    'F18': 0x81,
    'F19': 0x82,
    'F20': 0x83,
    'F21': 0x84,
    'F22': 0x85,
    'F23': 0x86,
    'F24': 0x87,
    'num_lock': 0x90,
    'scroll_lock': 0x91,
    'left_shift': 0xA0,
    'right_shift ': 0xA1,
    'left_control': 0xA2,
    'right_control': 0xA3,
    'left_menu': 0xA4,
    'right_menu': 0xA5,
    'browser_back': 0xA6,
    'browser_forward': 0xA7,
    'browser_refresh': 0xA8,
    'browser_stop': 0xA9,
    'browser_search': 0xAA,
    'browser_favorites': 0xAB,
    'browser_start_and_home': 0xAC,
    'volume_mute': 0xAD,
    'volume_Down': 0xAE,
    'volume_up': 0xAF,
    'next_track': 0xB0,
    'previous_track': 0xB1,
    'stop_media': 0xB2,
    'play/pause_media': 0xB3,
    'start_mail': 0xB4,
    'select_media': 0xB5,
    'start_application_1': 0xB6,
    'start_application_2': 0xB7,
    'attn_key': 0xF6,
    'crsel_key': 0xF7,
    'exsel_key': 0xF8,
    'play_key': 0xFA,
    'zoom_key': 0xFB,
    'clear_key': 0xFE,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE
}

char_mapping_us = {
    ' ': ['spacebar'],
    '!': ['left_shift', '1'],  #
    '@': ['left_shift', '2'],  #
    '#': ['left_shift', '3'],  #
    '$': ['left_shift', '4'],  #
    '%': ['left_shift', '5'],  #
    '^': ['left_shift', '6'],  #
    '&': ['left_shift', '7'],  #
    '*': ['left_shift', '8'],  #
    '(': ['left_shift', '9'],  #
    ')': ['left_shift', '0'],  #
    '{': ['left_shift', '['],
    '}': ['left_shift', ']'],
    '?': ['left_shift', '/'],
    ':': ['left_shift', ';'],
    '"': ['left_shift', "'"],
    '_': ['left_shift', '-'],
    '=': ['left_shift', '+'],
    '~': ['left_shift', '`'],
    '<': ['left_shift', ','],
    '>': ['left_shift', '.'],
}


def keybd_event(key: str, key_down: bool) -> None:
    """Sends a keyboard event to the system
    
    Arguments:
        key {str} -- The key to be sent
        key_down {bool} -- true for sending a key down event, false for sending a key up event
    """

    virtual_key_code = VK_CODE[key]
    event = 0 if key_down else win32con.KEYEVENTF_KEYUP
    win32api.keybd_event(virtual_key_code, win32api.MapVirtualKey(virtual_key_code, 0), event, 0)


def key_down(key: str):
    return keybd_event(key, True)


def key_up(key: str):
    return keybd_event(key, False)


def click_keys(*args, delay_between_keys: float = 0.05, key_down_hold_time: float = 0.05):
    """presses and releases the keys given in order

    accepts as many arguments as you want, e.g. click_keys('left_arrow', 'a','b').
    
    Keyword Arguments:
        delay_between_keys {float} -- time to wait before clicking the next key (default: {0.05})
        key_down_hold_time {float} -- time to wait to release the key (default: {0.05})
    """
    for i in args:
        key_down(i)
        time.sleep(key_down_hold_time)
        key_up(i)
        time.sleep(delay_between_keys)


def hold_keys(*args, delay_between_keys: float = 0.05):
    """Issues only a key-down event to the system, simulating a key hold

    accepts as many arguments as you want,
    e.g. hold_keys('left_arrow', 'a','b').
    
    Keyword Arguments:
        delay_between_keys {float} -- time to wait before holding the next key (default: {0.05})
    """
    for i in args:
        key_down(i)
        time.sleep(delay_between_keys)


def release_keys(*args, delay_between_keys: float = 0.05):
    """Issues only a key-up event to the system, releasing held keys

    accepts as many arguments as you want.
    e.g. release_keys('left_arrow', 'a','b').
    
    Keyword Arguments:
        delay_between_keys {float} -- time to wait before releasing the next key (default: {0.05})
    """
    for i in args:
        key_up(i)
        time.sleep(delay_between_keys)


def click_combination(*args, delay_between_keys: float = 0.05, key_down_hold_time: float = 0.05):
    """clicks all selected keys at the same time.

    accepts as many arguments as you want.
    e.g. click_combination('left_arrow', 'a','b').

    this is useful for issuing shortcut commands or shift commands.
    e.g. click_combination('ctrl', 'alt', 'del'), click_combination('shift','a')
    
    Keyword Arguments:
        delay_between_keys {float} -- time to wait before holding or releasing the next key (default: {0.05})
        key_down_hold_time {float} -- time to wait before releasing the keys (default: {0.05})
    """
    for i in args:
        key_down(i)
        time.sleep(delay_between_keys)

    time.sleep(key_down_hold_time)

    for i in args:
        key_up(i)
        time.sleep(delay_between_keys)


def type_sequence(string: Union[List[str], str], keyboard_char_dictionary: Dict[str, List[str]] = char_mapping_us):
    """Sends keystrokes to the system, writing what was given in the parameter
    
    Arguments:
        string {Union[List[str], str]} -- what to type
    
    Keyword Arguments:
        keyboard_char_dictionary {Dict[str, List[str]]} -- dictionary to use in order to make special characters that need to use Shift or some other key combination (default: {char_mapping_us})
    """
    for i in string:
        if i in keyboard_char_dictionary:
            click_keys(keyboard_char_dictionary[i])

        elif i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            click_keys('left_shift', i.lower())

        else:
            click_keys(i)


actions = {
    'type characters': type_sequence,
    'click key combination': click_combination,
    'hold keys': hold_keys,
    'release keys': release_keys,
    'click keys': click_keys
}
