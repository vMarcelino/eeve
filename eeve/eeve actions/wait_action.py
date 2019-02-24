from time import sleep
from eeve.taskinfo import TaskInfo


class IfAction:
    def run(self, parameter, end=False, inverse=False):
        if not end:
            if not ((not parameter) if inverse else parameter):
                if_count = 1
                for i, action in self.info.get_next_actions():
                    if action.name == 'end if':
                        if_count -= 1
                    elif action.name == 'if':
                        if_count += 1

                    if if_count == 0:
                        self.info.current_action_index = i
                        break

                else:  # if didn't hit break statement
                    self.info.current_action_index = len(self.info.actions)

                self.info.increment_action_index = False

    def set_task_info(self, info: TaskInfo):
        self.info = info


actions = {
    'wait': {
        'run': sleep
    },
    'if': {
        'class': IfAction,
        'task_info': IfAction.set_task_info
    },
    'end if': {
        'run': lambda: IfAction().run(parameter=None, end=True)
    }
}
