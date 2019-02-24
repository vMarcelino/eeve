from functools import wraps
from copy import deepcopy
from eeve.action import Action
from eeve.variable import VariableGroup
from eeve.taskinfo import TaskInfo
from typing import List

import travel_backpack

global_variables = VariableGroup()


def action_wrapper(actions: List[Action], debug=False):
    task_variables = VariableGroup()

    def start_task(**kwargs):
        local_variables = VariableGroup()

        task_info = TaskInfo(actions=actions, global_variables=global_variables, task_variables=task_variables, local_variables=local_variables)

        local_variables.update(kwargs)

        while task_info.current_action_index < len(task_info.actions):
            action = task_info.actions[task_info.current_action_index]
            _run_args = deepcopy(action.run_args)
            _run_kwargs = deepcopy(action.run_kwargs)
            if debug: print('------------------------------------------------------------processing act', action)

            for i, arg in enumerate(_run_args):
                if type(arg) is str:
                    if debug: print('------------------------------------------------------------processing arg', arg)
                    if arg.startswith('var$'):
                        arg = arg[3:]  # remove var prefix
                        if arg.startswith('$$$'):
                            if arg == '$$$vars':
                                _run_args[i] = global_variables.vars
                            else:
                                _run_args[i] = global_variables.get_var(arg[3:])
                        elif arg.startswith('$$'):
                            if arg == '$$vars':
                                _run_args[i] = task_variables.vars
                            else:
                                _run_args[i] = task_variables.get_var(arg[2:])
                        elif arg.startswith('$'):
                            if arg == '$vars':
                                _run_args[i] = local_variables.vars
                            else:
                                _run_args[i] = local_variables.get_var(arg[1:])

                    else:
                        if arg.startswith('$$$'):
                            if arg == '$$$vars':
                                _run_args[i] = global_variables.to_kwargs()
                            else:
                                _run_args[i] = global_variables.get(arg[3:], arg)
                        elif arg.startswith('$$'):
                            if arg == '$$vars':
                                _run_args[i] = task_variables.to_kwargs()
                            else:
                                _run_args[i] = task_variables.get(arg[2:], arg)
                        elif arg.startswith('$'):
                            if arg == '$vars':
                                _run_args[i] = local_variables.to_kwargs()
                            else:
                                _run_args[i] = local_variables.get(arg[1:], arg)

            for k, v in _run_kwargs.items():
                if type(v) is str:
                    #if v.startswith('$'):
                    #    if v == '$return_result':
                    #        _run_kwargs[k] = local_variables
                    #    else:
                    #        _run_kwargs[k] = local_variables.get(v[1:], v)

                    if debug: print('------------------------------------------------------------processing kwarg', v)
                    if v.startswith('var$'):
                        v = v[3:]  # remove var prefix
                        if v.startswith('$$$'):
                            if v == '$$$vars':
                                _run_kwargs[k] = global_variables.vars
                            else:
                                _run_kwargs[k] = global_variables.get_var(v[3:])
                        elif v.startswith('$$'):
                            if v == '$$vars':
                                _run_kwargs[k] = task_variables.vars
                            else:
                                _run_kwargs[k] = task_variables.get_var(v[2:])
                        elif v.startswith('$'):
                            if v == '$vars':
                                _run_kwargs[k] = local_variables.vars
                            else:
                                _run_kwargs[k] = local_variables.get_var(v[1:])

                    else:
                        if v.startswith('$$$'):
                            if v == '$$$vars':
                                _run_kwargs[k] = global_variables.to_kwargs()
                            else:
                                _run_kwargs[k] = global_variables.get(v[3:], v)
                        elif v.startswith('$$'):
                            if v == '$$vars':
                                _run_kwargs[k] = task_variables.to_kwargs()
                            else:
                                _run_kwargs[k] = task_variables.get(v[2:], v)
                        elif v.startswith('$'):
                            if v == '$vars':
                                _run_kwargs[k] = local_variables.to_kwargs()
                            else:
                                _run_kwargs[k] = local_variables.get(v[1:], v)

            if debug:
                print('call args:', _run_args, _run_kwargs)

            action.update_task_info(task_info)
            run_result = action.func(*_run_args, **_run_kwargs)

            if type(run_result) is dict:
                local_variables.update(run_result)

            if task_info.increment_action_index:
                task_info.current_action_index += 1

    return travel_backpack.except_and_print(start_task)
