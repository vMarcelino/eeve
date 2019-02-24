from eeve.variable import VariableGroup
from eeve.action import Action
from dataclasses import dataclass
from typing import List


@dataclass
class TaskInfo:
    actions: List[Action]
    global_variables: VariableGroup
    task_variables: VariableGroup
    local_variables: VariableGroup
    current_action_index: int = 0
    increment_action_index: bool = True

    def get_next_actions(self):
        return enumerate(self.actions[self.current_action_index:], self.current_action_index)