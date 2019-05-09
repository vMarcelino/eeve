from dataclasses import dataclass
from typing import Union, Any, Callable, List, Tuple
from eeve.wrapper import action_wrapper
from travel_backpack import check_and_raise, except_and_print


@dataclass
class ActionTemplate:
    name: str
    func: Callable
    init_result: Any = None
    task_info_getter: Union[Callable, None] = None
    init_func: Union[Callable, None] = None
    init_class: Union[Callable, None] = None

    @classmethod
    def make(cls, *action_init_args, name, action_info: Union[dict, Callable], **action_init_kwargs) -> 'ActionTemplate':
        self = cls(name=name, func=None)
        self.init_class = None
        if type(action_info) is dict:
            if 'class' in action_info:
                self.init_class = action_info['class']
            else:
                check_and_raise('run' in action_info, 'action_info must contain a "run" key with a callable as value', KeyError)
                self.func = action_info['run']
                if 'init' in action_info:
                    self.init_func = action_info['init']

            self.task_info_getter = action_info.get('task_info', None)

        else:
            self.init_class = action_info

        if self.init_class:
            self.init_func = self.init_class

        if self.init_func:
            self.init_result = self.init_func(*action_init_args, **action_init_kwargs)

        if self.init_class:
            check_and_raise(hasattr(self.init_class, 'run'), 'action_info must contain a "run" attribute', AttributeError)
            self.func = self.init_result.run

        return self

    @classmethod
    def copy_from(cls, obj) -> 'ActionTemplate':
        attrs = ['name', 'func', 'init_result', 'task_info_getter', 'init_func', 'init_class']
        r = {}
        for attr in attrs:
            if hasattr(obj, attr):
                r[attr] = getattr(obj, attr)
        return cls(**r)

    def reinitialize_with_args(self, *action_init_args, **action_init_kwargs):
        check_and_raise(self.init_func,
                        'Cannot initialize without an initialization function. Please provide an "init" key or a class on action_info', KeyError)
        self.init_result = self.init_func(*action_init_args, **action_init_kwargs)
        if self.init_class:
            self.func = self.init_result.run


@dataclass
class Action:
    '''
    A function with predetermined args that is
    executed in a task environment and raises no
    exceptions
    '''
    name: str
    func: Callable
    run_args: Union[list, tuple]
    run_kwargs: dict
    init_result: Any = None
    task_info_getter: Callable = None

    def run(self, *args, **kwargs):
        return except_and_print(self.func)(*args, **kwargs)

    def update_task_info(self, task_info) -> None:
        if self.task_info_getter is not None:
            self.task_info_getter(self.init_result, task_info)

    def __init__(self, *action_run_args, action_info: Union[ActionTemplate, dict, object], name=None, **action_run_kwargs):
        if type(action_info) is not ActionTemplate:
            check_and_raise(name, "parameter 'name' must be set when 'action_info' is not of type ActionTemplate", NameError)

            action_info = ActionTemplate.make(name=name, action_info=action_info)

        self.name = action_info.name
        self.func = action_info.func
        self.run_args = action_run_args
        self.run_kwargs = action_run_kwargs
        self.init_result = action_info.init_result
        self.task_info_getter = action_info.task_info_getter


@dataclass  # Yeah, I know... This class is horrible and shouldn't even exist.
class Task:  # I just wanted it to be organized as all the other classes
    """
    A list of Actions that are executed in sequence and
    in a separate thread. 
    This also carries variable information, which can be of
    one of the three types:


    Global Variables:
    ----------------
        \tVariables that are available to any
        \taction at any given moment.
        \tThese variables persist until the process ends.


    Task Variables:
    --------------
        \tVariables that are only available to
        \tactions inside it's task at any given moment.
        \tThese variables persist after the task ends, but
        \tare released when the process ends.
        \tThis means that one action can access a
        \tvariable created by an older run of the task.


    Local Variables:
    ---------------
        \tVariables that are only available to
        \tactions inside it's task when it is running.
        \tThese variables are released when the task or
        \tthe process ends.
    """
    start: Callable

    def __init__(self, actions: List[Action], debug: bool = False, verbose=1):
        self.start = action_wrapper(actions=actions, debug=debug, verbose=verbose)


@dataclass
class TriggerTemplate:
    name: str
    register: Callable
    unregister: Callable


@dataclass
class Trigger:
    name: str
    _register: Callable
    register: Callable
    unregister: Callable
    args: list
    kwargs: dict

    def __init__(self, *args, name: str, register: Callable, unregister: Callable, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self._register = register
        self.register = lambda task: register(task, *self.args, **self.kwargs)
        self.unregister = unregister

    @classmethod
    def make(cls, *args, template: TriggerTemplate, **kwargs) -> 'Trigger':
        return cls(*args, name=template.name, register=template.register, unregister=template.unregister, **kwargs)


@dataclass
class Event:
    '''Links triggers with a task and starts all the triggers
    
    Is recommended to use a single trigger for each event.\n
    Multiple triggers are supported for convenience so that
    all triggers can be unregistered at once for a given task.
    '''
    unregister_info: List[Tuple[Callable, Any]]

    def __init__(self, triggers: List[Trigger], task: Task):
        self.unregister_info = []
        for trigger in triggers:
            self.unregister_info.append((trigger.unregister, trigger.register(task.start)))

    def unregister(self):
        for unregister_func, trigger_output_result in self.unregister_info:
            unregister_func(trigger_output_result)