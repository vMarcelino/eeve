from functools import wraps
from copy import deepcopy
from eeve.action import Action

global_variables = dict()


def action_wrapper(actions: list, debug=False):
    task_variables = dict()

    def decorator(**kwargs):
        local_variables = kwargs

        for action in actions:
            _run_args = deepcopy(action.run_args)
            _run_kwargs = deepcopy(action.run_kwargs)
            for i, arg in enumerate(_run_args):
                if arg.startswith('$$$'):
                    _run_args[i] = local_variables.get(arg[3:], arg)
                if arg.startswith('$$'):
                    _run_args[i] = local_variables.get(arg[2:], arg)
                if arg.startswith('$'):
                    if arg == '$return_result':
                        _run_args[i] = local_variables
                    else:
                        _run_args[i] = local_variables.get(arg[1:], arg)

            for k, v in _run_kwargs.items():
                if type(v) is str and v.startswith('$'):
                    if v == '$return_result':
                        _run_kwargs[k] = local_variables
                    else:
                        _run_kwargs[k] = local_variables.get(v[1:], v)
            if debug:
                print('call args:', _run_args, _run_kwargs)

            run_result = action.func(*_run_args, **_run_kwargs)

            if type(run_result) is dict:
                local_variables.update(run_result)

    return decorator