"""eeve - A flexible, powerfull and simple event trigger"""

__version__ = '0.1.0'
__author__ = 'Victor Marcelino <victor.fmarcelino@gmail.com>'
__all__ = []

import travel_backpack
import os

import eeve.helpers as helpers
from eeve.importer import import_from_folder
from eeve.wrapper import action_wrapper
from eeve.action import Action
import eeve.mappings as mappings

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
                event = mappings.remap(event)
                trigger, raw_actions = helpers.strip_split(event, mappings.char_map['->'], maxsplit=1)

                trigger, trigger_args, trigger_kwargs = helpers.process_args(trigger, return_init_args=False)

                raw_actions = helpers.strip_split(raw_actions, mappings.char_map[';'])
                actions = []
                for action in raw_actions:
                    action_name, action_init_args, action_init_kwargs, action_run_args, action_run_kwargs = helpers.process_args(
                        action, return_init_args=True)

                    _action = all_actions[action_name]
                    action_init_result = None
                    action_run = None
                    action_task_info_getter = None

                    if type(_action) is dict:
                        if 'class' in _action:
                            action_init_result = _action['class'](*action_init_args, **action_init_kwargs)
                            action_run = action_init_result.run
                        else:
                            if 'init' in _action:
                                action_init_result = _action['init'](*action_init_args, **action_init_kwargs)
                            action_run = _action['run']

                        action_task_info_getter = _action.get('task_info', None)

                    action_run = travel_backpack.except_and_print(action_run)
                    act = Action(
                        func=action_run,
                        run_args=action_run_args,
                        run_kwargs=action_run_kwargs,
                        init_result=action_init_result,
                        task_info_getter=action_task_info_getter,
                        name=action_name)
                    actions.append(act)
                    #action_run = action_wrapper(action_run, action_run_args, action_run_kwargs, debug=show_traceback)

                task = action_wrapper(actions, debug=show_traceback)
                all_triggers[trigger](task, *trigger_args, **trigger_kwargs)

            except Exception as ex:
                print('invalid event:', (ex if not show_traceback else travel_backpack.format_exception_string(ex)))

    print('--all events loaded--')