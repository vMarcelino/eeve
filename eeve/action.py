from dataclasses import dataclass
from typing import Union, Any, Callable


@dataclass
class Action:
    func: Callable
    name: str
    run_args: Union[list, tuple]
    run_kwargs: dict
    init_result: Any = None
    task_info_getter: Callable = None

    def update_task_info(self, task_info):
        if self.task_info_getter is not None:
            self.task_info_getter(self.init_result, task_info)