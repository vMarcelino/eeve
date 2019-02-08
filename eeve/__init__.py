"""eeve - A flexible, powerfull and simple event trigger"""

__version__ = '0.1.0'
__author__ = 'Victor Marcelino <victor.fmarcelino@gmail.com>'
__all__ = []

import travel_backpack
import os

import eeve.helpers as helpers
from eeve.importer import import_from_folder

all_triggers, all_actions = {}, {}

#yapf: disable
all_events = [
    'display: off   -> set power plan: Power saver',

    'display: on    -> start process: cmd, /C, echo oi&&pause, windowed=True',
    'display: on    -> set power plan: Balanced', 'display: on -> rest request: GET, http://192.168.10.11:2280/surveilance/stop, wait_time=1',

    'session end    -> rest request: GET, http://192.168.10.11:2280/surveilance/start',
    'system suspend -> rest request: GET, http://192.168.10.11:2280/surveilance/start'
]
#yapf: enable


def main():
    script_root = os.path.dirname(os.path.realpath(__file__))
    modules = import_from_folder(os.path.join(script_root, 'eeve triggers'))
    for module in modules:
        try:
            triggers = getattr(module, 'triggers', None)
            for trigger_name, trigger in triggers.items():
                print('loading', trigger_name)
                all_triggers[trigger_name] = trigger
        except Exception as ex:
            print('invalid action module:', ex)
    print('--all triggers loaded--')

    modules = import_from_folder(os.path.join(script_root, 'eeve actions'))
    for module in modules:
        try:
            actions = getattr(module, 'actions', None)
            for action_name, action in actions.items():
                print('loading', action_name)
                all_actions[action_name] = action
        except Exception as ex:
            print('invalid action module:', ex)
    print('--all actions loaded--')

    for event in all_events:
        print('loading', event)
        try:
            trigger, action = helpers.strip_split(event, '->', maxsplit=1)

            def process_args(x):
                args = []
                kwargs = {}
                if ':' in x:
                    x, _args = helpers.strip_split(x, ':', maxsplit=1)
                    _args = helpers.strip_split(_args, ',')
                    for arg in _args:
                        if '=' in arg:
                            k, v = helpers.strip_split(arg, '=', maxsplit=1)
                            kwargs[k] = helpers.get_true_value(v)
                        else:
                            args.append(helpers.get_true_value(arg))

                return x, args, kwargs

            trigger, trigger_args, trigger_kwargs = process_args(trigger)
            action, action_args, action_kwargs = process_args(action)

            action = all_actions[action](*action_args, **action_kwargs)
            all_triggers[trigger](travel_backpack.except_and_print(action.run), *trigger_args, **trigger_kwargs)
        except Exception as ex:
            print('invalid event:', ex)
    print('--all events loaded--')
