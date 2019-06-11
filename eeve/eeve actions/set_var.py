from eeve.variable import Variable, get_var_name
from eeve.taskinfo import TaskInfo
from datetime import datetime


class SetVar:
    def __init__(self):
        self.info: TaskInfo = None

    def run(self, var: 'Union[Variable, str]', value: 'Any', scope: str = 'local', *args):
        """Sets the variable to a given value.

        'var' can either be a Variable reference or str. If it is a Variable reference,
        the scope parameter is ignored

        If 'value' is {now}, the variable is set to current date and time

        If 'value' is {expression:someExpressionHere}, arguments are used to format the expression
        and the expression is evaluated using python's eval. USE CAREFULLY
        
        Arguments:
            var {Union[Variable, str]} -- The variable to set
            value {Any} -- The value to set the variable
        
        Keyword Arguments:
            scope {str} -- Can either be 'local', 'task' or 'global', case insensitive (default: {'local'})
        
        Raises:
            Exception: In case the scope is invalid
        """
        if value == '{now}':
            value = datetime.now()
        elif value.startswith('{expression:') and value.endswith('}'):
            value = value[12:-1]  # remove the beggining and last '}'
            value.format(*args)
            value = eval(value)

        if type(var) is str:
            vn = get_var_name(var)
            scope = scope.lower()
            if scope == 'local':
                vn = 'var$' + vn
                self.info.get_var(vn).value = value
            elif scope == 'task':
                vn = 'var$$' + vn
                self.info.get_var(vn).value = value
            elif scope == 'global':
                vn = 'var$$$' + vn
                self.info.get_var(vn).value = value
            else:
                raise Exception('Scope must be either "local", "task" or "global"')
        else:
            var.value = value

    def set_task_info(self, info: TaskInfo):
        #print('info set')
        self.info: TaskInfo = info


actions = {'set variable': {'class': SetVar, 'task_info': SetVar.set_task_info}}
