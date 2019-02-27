from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Event:
    unregister_func: Callable
    trigger_output_result: Any = None

    def unregister(self):
        self.unregister_func(self.trigger_output_result)
