from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QAbstractListModel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QMessageBox  # pylint: disable=no-name-in-module
import inspect

import eeve
from eeve.base_classes import Event, Trigger, Task, Action
from .. import GuiController  # pylint: disable=relative-beyond-top-level
from eeve import database


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
        for i, trigger_arg in enumerate(self.trigger.args):
            value = {"value": str(trigger_arg), 'tag': i}
            self.invoke(result, 'addItem', value)

    def unload_page(self):
        print('unloading page')
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
        #if '=' in value:

        self.trigger.args = list(self.trigger.args)
        self.trigger.args[index] = value
        self.database_ref.arguments[index].value = value

    @pyqtSlot()
    def addTriggerArgument(self):
        root = self.main_controller.engine.rootObjects()
        root = root[0]
        result = root.findChild(QAbstractListModel, "listmodelargs")

        i = len(self.trigger.args)
        self.trigger.args = list(self.trigger.args)
        self.trigger.args.append(f'arg {i}')
        self.database_ref.arguments.append(database.TriggerArgument(value=f'arg {i}'))

        self.invoke(result, "addItem", {'value': self.trigger.args[i], 'tag': i})

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
