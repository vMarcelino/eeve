import os
import importlib
import travel_backpack as helpers
from functools import wraps

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


def strip_split(s, *args, **kwargs):
    return list(map(lambda x: x.strip(), s.split(*args, **kwargs)))


def try_cast(tp, obj):
    try:
        tp(obj)
        return True
    except:
        return False


def get_true_value(x):
    if try_cast(int, x):
        return int(x)
    elif try_cast(float, x):
        return float(x)
    elif x.lower in ['true', 'false']:
        return bool(x)
    else:
        return x


def main():
    modules = import_from_folder(os.path.join('.', 'eeve triggers'))
    for module in modules:
        try:
            triggers = getattr(module, 'triggers', None)
            for trigger_name, trigger in triggers.items():
                print('loading', trigger_name)
                all_triggers[trigger_name] = trigger
        except Exception as ex:
            print('invalid action module:', ex)
    print('--all triggers loaded--')

    modules = import_from_folder(os.path.join('.', 'eeve actions'))
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
            trigger, action = strip_split(event, '->', maxsplit=1)

            def process_args(x):
                args = []
                kwargs = {}
                if ':' in x:
                    x, _args = strip_split(x, ':', maxsplit=1)
                    _args = strip_split(_args, ',')
                    for arg in _args:
                        if '=' in arg:
                            k, v = strip_split(arg, '=', maxsplit=1)
                            kwargs[k] = get_true_value(v)
                        else:
                            args.append(get_true_value(arg))

                return x, args, kwargs

            trigger, trigger_args, trigger_kwargs = process_args(trigger)
            action, action_args, action_kwargs = process_args(action)

            action = all_actions[action](*action_args, **action_kwargs)
            all_triggers[trigger](helpers.except_and_print(action.run), *trigger_args, **trigger_kwargs)
        except Exception as ex:
            print('invalid event:', ex)
    print('--all events loaded--')


def import_from_folder(folder):
    imported_files = []
    import sys
    folder = os.path.abspath(folder)
    if folder not in sys.path:
        sys.path.insert(0, folder)

    for file_obj in os.listdir(folder):
        print('inspecting', file_obj)
        file_obj = os.path.join(folder, file_obj)
        if os.path.isfile(file_obj):
            if file_obj.endswith('.py'):
                module_name = os.path.splitext(os.path.basename(file_obj))[0]
                print('==> importing', module_name)
                imported_files.append(importlib.import_module(module_name))

        elif os.path.isdir(file_obj):
            if os.path.basename(file_obj) not in ['.', '..', '__pycache__']:
                module_name = os.path.basename(file_obj)
                print('--> importing', module_name)
                imported_files.append(importlib.import_module(module_name))

    return imported_files


if __name__ == "__main__":
    main()