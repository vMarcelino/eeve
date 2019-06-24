from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QAbstractListModel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QMessageBox  # pylint: disable=no-name-in-module
import inspect
from typing import Any, List
from dataclasses import dataclass

import eeve
from eeve.base_classes import Event, Task, Action
from .. import GuiController  # pylint: disable=relative-beyond-top-level
from eeve import database, helpers


@dataclass
class ParamInfo:
    required: list
    optional: list
    accept_args: bool
    accept_kwargs: bool


@dataclass
class Argument:
    value: Any
    key: str = None


class EditActionController(GuiController):
    def load_page(self, action: Action, database_ref: database.Action):

        self.action = action
        self.database_ref = database_ref
        if self.action is None:
            self.action = Action(action_info=eeve.action_templates['start gui'])

        root = self.main_controller.engine.rootObjects()
        root = root[0]
        result = root.findChild(QAbstractListModel, "actionListModel")
        self.invoke(result, 'clearItems', None)
        index = 0
        self.param_info = {}
        for i, action_name in enumerate(eeve.action_templates):
            ac = eeve.action_templates[action_name].func
            print(action_name)
            accept_args = False
            accept_kwargs = False
            req_args = []
            opt_args = []
            try:
                sig = inspect.signature(ac)
                for par in sig.parameters:
                    p = sig.parameters[par]
                    if p.kind is p.VAR_POSITIONAL:
                        accept_args = True
                    elif p.kind is p.VAR_KEYWORD:
                        accept_kwargs = True
                    elif p.default is p.empty:
                        req_args.append([p.name, p.annotation])
                    else:
                        opt_args.append([p.name, p.annotation, p.default])
                    pass
            except:
                accept_args = accept_kwargs = True

            self.param_info[action_name] = ''
            if ac.__doc__:
                self.param_info[action_name] += ac.__doc__ + '\n' + ('-' * 25) + '\n\n'

            if req_args:
                self.param_info[action_name] += '\trequired:\n'
                for arg, annotation in req_args:
                    ant = '?'
                    if annotation != inspect._empty:
                        if hasattr(annotation, '__name__'):
                            ant = annotation.__name__
                        else:
                            ant = str(annotation)

                    self.param_info[action_name] += f'\t\tname: {arg},    type: {ant}\n'
            if opt_args:
                self.param_info[action_name] += '\toptional:\n'
                for arg, annotation, value in opt_args:
                    ant = '?'
                    if annotation != inspect._empty:
                        if hasattr(annotation, '__name__'):
                            ant = annotation.__name__
                        else:
                            ant = str(annotation)

                    self.param_info[action_name] += f'\t\tname: {arg},   default: {value},    type: {ant}\n'

            if accept_args:
                self.param_info[action_name] += '\taccepts args\n'
            if accept_kwargs:
                self.param_info[action_name] += '\taccepts kwargs\n'

            self.invoke(result, 'addItem', str(action_name))
            if action_name == self.action.name:
                index = i

        result = root.findChild(QObject, "actionsComboBox")
        result.setProperty("currentIndex", index)

        result = root.findChild(QAbstractListModel, "listmodelargs")

        self.arguments: List[Argument] = []
        for action_arg in self.action.run_args:
            self.arguments.append(Argument(value=str(action_arg)))

        for k, v in self.action.run_kwargs.items():
            self.arguments.append(Argument(key=k, value=str(v)))

        for i, action_arg in enumerate(self.arguments):
            if action_arg.key is not None:
                value = {"value": action_arg.key + '=' + str(action_arg.value), 'tag': i}
            else:
                value = {"value": str(action_arg.value), 'tag': i}
            self.invoke(result, 'addItem', value)

    def unload_page(self):
        print('unloading page')
        self.action.run_args = list(self.action.run_args)  # make sure it is a list
        self.action.run_args.clear()
        self.action.run_kwargs.clear()
        self.database_ref.arguments.clear()
        for arg in self.arguments:
            if arg.key:
                self.action.run_kwargs[arg.key] = helpers.get_true_value(arg.value)
                self.database_ref.arguments.append(database.ActionArgument(key=arg.key, value=arg.value))
            else:
                self.action.run_args.append(helpers.get_true_value(arg.value))
                self.database_ref.arguments.append(database.ActionArgument(value=arg.value))

        return self.action, self.database_ref

    @pyqtSlot()
    def showParametersInfo(self):
        QMessageBox.information(None, 'Ajuda: Parâmetros', self.param_info[self.action.name])

    @pyqtSlot(str)
    def actionChanged(self, action_name):
        self.action = Action(*self.action.run_args,
                             action_info=eeve.action_templates[action_name],
                             **self.action.run_kwargs)
        self.database_ref.name = action_name
        print(self.action)

    @pyqtSlot(int, str)
    def argsChanged(self, index, value):
        print(index, value)
        key = None
        if '=' in value:  # if is kwarg
            key, value = value.split('=', maxsplit=1)

        if key:  # if is not None nor empty
            self.arguments[index] = Argument(key=key, value=value)
        else:
            self.arguments[index] = Argument(value=value)

    @pyqtSlot()
    def addActionArgument(self):
        root = self.main_controller.engine.rootObjects()
        root = root[0]
        result = root.findChild(QAbstractListModel, "listmodelargs")

        i = len(self.arguments)
        self.arguments.append(Argument(value=f'arg {i}'))

        self.invoke(result, "addItem", {'value': self.arguments[i].value, 'tag': i})

    @pyqtSlot(int)
    def deleteArg(self, index):
        root = self.main_controller.engine.rootObjects()
        root = root[0]
        result = root.findChild(QAbstractListModel, "listmodelargs")
        self.invoke(result, "clearItems", None)

        self.action.run_args: list = list(self.action.run_args)
        self.action.run_args.pop(index)
        i = self.database_ref.arguments.pop(index)
        #delete i

        self.load_page(action=self.action, database_ref=self.database_ref)


def print_child(obj, i=0):
    print('-' * 4 * i, obj.property("objectName"), obj)
    for dp in QObject.dynamicPropertyNames(obj):
        print('-' * 4 * i, 'prop:', dp, obj.property(dp))

    for c in obj.children():
        print_child(c, i + 1)
