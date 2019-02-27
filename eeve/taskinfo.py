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
        return enumerate(self.actions[self.current_action_index + 1:], self.current_action_index + 1)

    def get_var(self, var_name: str):
        original_var_name = var_name
        is_var = var_name.startswith('var$')

        class Scopes:
            Global = self.global_variables
            Task = self.task_variables
            Local = self.local_variables

        scope = Scopes.Local

        if is_var:
            var_name = var_name[3:]

        if var_name.startswith('$$$'):
            scope = Scopes.Global
            var_name = var_name[3:]
        elif var_name.startswith('$$'):
            scope = Scopes.Task
            var_name = var_name[2:]
        elif var_name.startswith('$'):
            scope = Scopes.Local
            var_name = var_name[1:]

        if is_var:
            if var_name == 'vars':
                return scope.vars
            else:
                return scope.get_var(var_name)
        else:
            if var_name == 'vars':
                return scope.to_kwargs()
            else:
                return scope.get(var_name, original_var_name)

    def has_var(self, var_name: str) -> bool:
        is_var = var_name.startswith('var$')

        class Scopes:
            Global = self.global_variables
            Task = self.task_variables
            Local = self.local_variables

        scope = Scopes.Local

        if is_var:
            var_name = var_name[3:]
        if var_name.startswith('$$$'):
            scope = Scopes.Global
            var_name = var_name[3:]
        elif var_name.startswith('$$'):
            scope = Scopes.Task
            var_name = var_name[2:]
        elif var_name.startswith('$'):
            scope = Scopes.Local
            var_name = var_name[1:]

        return var_name in scope.vars
