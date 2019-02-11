"""eeve - A flexible, powerfull and simple event trigger"""

__version__ = '0.1.0'
__author__ = 'Victor Marcelino <victor.fmarcelino@gmail.com>'
__all__ = []

import travel_backpack
import os

import eeve.helpers as helpers
from eeve.importer import import_from_folder

all_triggers, all_actions = {}, {}


def main():
    script_root = os.path.dirname(os.path.realpath(__file__))
    load_triggers(os.path.join(script_root, 'eeve triggers'))
    load_actions(os.path.join(script_root, 'eeve actions'))
    load_events(os.path.join(script_root, 'eeve events.txt'))


def load_triggers(path):
    modules = import_from_folder(path)
    for module in modules:
        try:
            triggers = getattr(module, 'triggers', None)
            for trigger_name, trigger in triggers.items():
                print('loading', trigger_name)
                all_triggers[trigger_name] = trigger
        except Exception as ex:
            print('invalid action module:', ex)
    print('--all triggers loaded--')


def load_actions(path):
    modules = import_from_folder(path)
    for module in modules:
        try:
            actions = getattr(module, 'actions', None)
            for action_name, action in actions.items():
                print('loading', action_name)
                all_actions[action_name] = action
        except Exception as ex:
            print('invalid action module:', ex)
    print('--all actions loaded--')


def load_events(path):
    with open(path) as f:
        all_events = f.read().split('\n')

    for event in all_events:
        if event and not event.startswith('#'):
            print(f'loading [{event}]')
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