from functools import wraps
from copy import deepcopy


def action_wrapper(f, run_args, run_kwargs):
    @wraps(f)
    def decorator(**kwargs):
        _run_args = deepcopy(run_args)
        _run_kwargs = deepcopy(run_kwargs)

        for i, arg in enumerate(_run_args):
            if arg.startswith('$'):
                if arg == '$return_result':
                    _run_args[i] = kwargs
                else:
                    _run_args[i] = kwargs.get(arg[1:], arg)

        for k, v in _run_kwargs.items():
            if v.startswith('$'):
                if v == '$return_result':
                    _run_kwargs[k] = kwargs
                else:
                    _run_kwargs[k] = kwargs.get(v[1:], v)

        return f(*_run_args, **_run_kwargs)

    return decorator