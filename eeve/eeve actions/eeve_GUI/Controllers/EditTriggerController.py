from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QAbstractListModel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QMessageBox  # pylint: disable=no-name-in-module
import inspect
from typing import Any, List
from dataclasses import dataclass

import eeve
from eeve.base_classes import Event, Trigger, Task, Action
from .. import GuiController  # pylint: disable=relative-beyond-top-level
from eeve import database, helpers


@dataclass
class Argument:
    value: Any
    key: str = None


class EditTriggerController(GuiController):
    def load_page(self, trigger: Trigger, database_ref: database.Trigger):

        self.trigger = trigger
        self.database_ref = database_ref

        if self.trigger is None:
            self.trigger = Trigger.make(template=eeve.trigger_templates['on eeve startup'])

        root = self.main_controller.engine.rootObjects()
        root = root[0]
        result = root.findChild(QAbstractListModel, "tlm")
        self.invoke(result, 'clearItems', None)
        index = 0
        self.param_info = {}
        for i, trigger_name in enumerate(eeve.trigger_templates):
            ac = eeve.trigger_templates[trigger_name].register
            print(trigger_name)
            accept_args = False
            accept_kwargs = False
            req_args = []
            opt_args = []
            try:
                sig = inspect.signature(ac)
                for param_number, par in enumerate(sig.parameters):
                    if param_number == 0:
                        continue  # ignore first param (action)

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

            self.param_info[trigger_name] = ''
            if ac.__doc__:
                self.param_info[trigger_name] += ac.__doc__ + '\n' + ('-' * 25) + '\n\n'

            if req_args:
                self.param_info[trigger_name] += '\trequired:\n'
                for arg, annotation in req_args:
                    ant = '?'
                    if annotation != inspect._empty:
                        if hasattr(annotation, '__name__'):
                            ant = annotation.__name__
                        else:
                            ant = str(annotation)

                    self.param_info[trigger_name] += f'\t\tname: {arg},    type: {ant}\n'
            if opt_args:
                self.param_info[trigger_name] += '\toptional:\n'
                for arg, annotation, value in opt_args:
                    ant = '?'
                    if annotation != inspect._empty:
                        if hasattr(annotation, '__name__'):
                            ant = annotation.__name__
                        else:
                            ant = str(annotation)

                    self.param_info[trigger_name] += f'\t\tname: {arg},   default: {value},    type: {ant}\n'

            if accept_args:
                self.param_info[trigger_name] += '\taccepts args\n'
            if accept_kwargs:
                self.param_info[trigger_name] += '\taccepts kwargs\n'

            self.invoke(result, 'addItem', str(trigger_name))
            if trigger_name == self.trigger.name:
                index = i

        result = root.findChild(QObject, "triggersComboBox")
        result.setProperty("currentIndex", index)

        result = root.findChild(QAbstractListModel, "listmodelargs")

        self.arguments: List[Argument] = []
        for trigger_arg in self.trigger.args:
            self.arguments.append(Argument(value=str(trigger_arg)))

        for k, v in self.trigger.kwargs.items():
            self.arguments.append(Argument(key=k, value=str(v)))

        for i, trigger_arg in enumerate(self.arguments):
            if trigger_arg.key is not None:
                value = {"value": trigger_arg.key + '=' + str(trigger_arg.value), 'tag': i}
            else:
                value = {"value": str(trigger_arg.value), 'tag': i}
            self.invoke(result, 'addItem', value)

    def unload_page(self):
        print('unloading page')
        self.trigger.args = list(self.trigger.args)  # make sure it is a list
        self.trigger.args.clear()
        self.trigger.kwargs.clear()
        self.database_ref.arguments.clear()
        for arg in self.arguments:
            if arg.key:
                self.trigger.kwargs[arg.key] = helpers.get_true_value(arg.value)
                self.database_ref.arguments.append(database.TriggerArgument(key=arg.key, value=arg.value))
            else:
                self.trigger.args.append(helpers.get_true_value(arg.value))
                self.database_ref.arguments.append(database.TriggerArgument(value=arg.value))

        return self.trigger, self.database_ref

    @pyqtSlot()
    def showParametersInfo(self):
        QMessageBox.information(None, 'Ajuda: Parâmetros', self.param_info[self.trigger.name])

    @pyqtSlot(str)
    def triggerChanged(self, trigger_name):
        t = self.trigger
        self.trigger = Trigger.make(*t.args, template=eeve.trigger_templates[trigger_name], **t.kwargs)
        t = None
        print(self.trigger)
        self.database_ref.name = trigger_name

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
    def addTriggerArgument(self):
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

        self.trigger.args: list = list(self.trigger.args)
        self.trigger.args.pop(index)
        i = self.database_ref.arguments.pop(index)
        #delete i

        self.load_page(trigger=self.trigger, database_ref=self.database_ref)


def print_child(obj, i=0):
    print('-' * 4 * i, obj.property("objectName"), obj)
    for dp in QObject.dynamicPropertyNames(obj):
        print('-' * 4 * i, 'prop:', dp, obj.property(dp))

    for c in obj.children():
        print_child(c, i + 1)
