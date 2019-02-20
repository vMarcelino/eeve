"""eeve - A flexible, powerfull and simple event trigger"""

__version__ = '0.1.0'
__author__ = 'Victor Marcelino <victor.fmarcelino@gmail.com>'
__all__ = []

import travel_backpack
import os

import eeve.helpers as helpers
from eeve.importer import import_from_folder
from eeve.wrapper import action_wrapper

all_triggers, all_actions = {}, {}


def main():
    script_root = os.path.dirname(os.path.realpath(__file__))
    load_triggers(os.path.join(script_root, 'eeve triggers'))
    load_actions(os.path.join(script_root, 'eeve actions'))

    load_triggers(os.path.join(script_root, 'eeve plugins'))
    load_actions(os.path.join(script_root, 'eeve plugins'))

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
            show_traceback = False
            print(f'loading [{event}]')
            if event.startswith('[test]'):
                show_traceback = True
                event = event[len('[test]'):]
            try:
                trigger, action_name = helpers.strip_split(event, '->', maxsplit=1)

                trigger, trigger_args, trigger_kwargs = helpers.process_args(trigger, return_init_args=False)
                action_name, action_init_args, action_init_kwargs, action_run_args, action_run_kwargs = helpers.process_args(
                    action_name, return_init_args=True)

                _action = all_actions[action_name]
                action_init = None
                action_run = None
                if type(_action) is dict:
                    action_init = _action.get('init', None)
                    action_run = _action['run']

                else:
                    action_init = _action

                if action_init is not None:
                    action_init = action_init(*action_init_args, **action_init_kwargs)
                if action_run is None:
                    action_run = action_init.run

                action_run = action_wrapper(action_run, action_run_args, action_run_kwargs, debug=show_traceback)
                action_run = travel_backpack.except_and_print(action_run)

                all_triggers[trigger](action_run, *trigger_args, **trigger_kwargs)

            except Exception as ex:
                print('invalid event:', (ex if not show_traceback else travel_backpack.format_exception_string(ex)))

    print('--all events loaded--')