"""eeve - A flexible, powerfull and simple event trigger"""

__version__ = '0.2.0'
__author__ = 'Victor Marcelino <victor.fmarcelino@gmail.com>'
__all__ = []

import travel_backpack
import os

import eeve.helpers as helpers
from eeve.importer import import_from_folder
from eeve.wrapper import action_wrapper
from eeve.action import Action
from eeve.event import Event
import eeve.mappings as mappings

all_triggers, all_actions = {}, {}
all_events = []


def main():
    print()
    script_root = os.path.dirname(os.path.realpath(__file__))
    load_triggers(os.path.join(script_root, 'eeve triggers'))
    load_actions(os.path.join(script_root, 'eeve actions'))

    load_triggers(os.path.join(script_root, 'eeve plugins'))
    load_actions(os.path.join(script_root, 'eeve plugins'))

    with open(os.path.join(script_root, 'eeve events.txt')) as f:
        _all_events = f.read().replace('|||\n', '').split('\n')
    load_events(_all_events)


def unload_trigger(trigger_name):
    if trigger_name in all_triggers:
        del all_triggers[trigger_name]


def unload_action(action_name):
    if action_name in all_actions:
        del all_actions[action_name]


def load_triggers(path):
    print('--loading triggers--')
    modules = import_from_folder(path)
    for module in modules:
        try:
            triggers = getattr(module, 'triggers', dict())
            for trigger_name, trigger in triggers.items():
                print('loading', trigger_name)
                if type(trigger) is dict:
                    all_triggers[trigger_name] = trigger
                else:
                    all_triggers[trigger_name] = {'register': trigger, 'unregister': trigger.unregister}
        except Exception as ex:
            print('invalid trigger module:', ex)
    print('--triggers loaded--')
    print()
    print()


def load_actions(path):
    print('--loading actions--')
    modules = import_from_folder(path)
    for module in modules:
        try:
            actions = getattr(module, 'actions', dict())
            for action_name, action in actions.items():
                print('loading', action_name)
                all_actions[action_name] = action
        except Exception as ex:
            print('invalid action module:', ex)
    print('--actions loaded--')
    print()
    print()


def load_events(_all_events: list):
    print('--loading events--')
    for event in _all_events:
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
                                init_act = _action['init']
                                action_init_result = init_act(*action_init_args, **action_init_kwargs)
                            action_run = _action['run']

                        action_task_info_getter = _action.get('task_info', None)

                    else:
                        action_init_result = _action(*action_init_args, **action_init_kwargs)
                        action_run = action_init_result.run

                    #print(action_run)
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
                event = Event(all_triggers[trigger]['unregister'])
                event.trigger_output_result = all_triggers[trigger]['register'](task, *trigger_args, **trigger_kwargs)
                all_events.append(event)

            except Exception as ex:
                print('invalid event:', (ex if not show_traceback else travel_backpack.format_exception_string(ex)))

    print('--events loaded--')
    print()
    print()