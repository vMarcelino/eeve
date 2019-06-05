from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QAbstractListModel  # pylint: disable=no-name-in-module

import eeve
from eeve.base_classes import Event, Task, Action
from .. import GuiController  # pylint: disable=relative-beyond-top-level
import inspect


class EditActionController(GuiController):
    def load_page(self, action: Action = None):

        self.action = action
        if self.action is None:
            self.action = Action(action_info=eeve.action_templates['start gui'])

        root = self.main_controller.engine.rootObjects()
        root = root[0]
        result = root.findChild(QAbstractListModel, "actionListModel")
        index = 0
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
            if req_args:
                print('\trequired:')
                for arg, annotation in req_args:
                    ant = '?'
                    if annotation != inspect._empty:
                        if hasattr(annotation, '__name__'):
                            ant = annotation.__name__
                        else:
                            ant = str(annotation)

                    print('\t\tname:', arg, ', type:', ant)
            if opt_args:
                print('\toptional:')
                for arg, annotation, value in opt_args:
                    ant = '?'
                    if annotation != inspect._empty:
                        if hasattr(annotation, '__name__'):
                            ant = annotation.__name__
                        else:
                            ant = str(annotation)

                    print('\t\tname:', arg, ', type:', ant, ', value:',value)
            if accept_args:
                print('\taccepts args')
            if accept_kwargs:
                print('\taccepts kwargs')

            self.invoke(result, 'addItem', str(action_name))
            if action_name == self.action.name:
                index = i

        result = root.findChild(QObject, "actionsComboBox")
        result.setProperty("currentIndex", index)

        result = root.findChild(QAbstractListModel, "listmodelargs")
        for i, action_arg in enumerate(self.action.run_args):
            value = {"value": str(action_arg), 'tag': i}
            self.invoke(result, 'addItem', value)

    def unload_page(self):
        print('unloading page')
        return self.action

    @pyqtSlot(str)
    def actionChanged(self, action_name):
        self.action = Action(*self.action.run_args,
                             action_info=eeve.action_templates[action_name],
                             **self.action.run_kwargs)
        print(self.action)

    @pyqtSlot(int, str)
    def argsChanged(self, index, value):
        print(index, value)
        self.action.run_args = list(self.action.run_args)
        self.action.run_args[index] = value

    @pyqtSlot()
    def addActionArgument(self):
        root = self.main_controller.engine.rootObjects()
        root = root[0]
        result = root.findChild(QAbstractListModel, "listmodelargs")

        i = len(self.action.run_args)
        self.action.run_args = list(self.action.run_args)
        self.action.run_args.append(f'arg {i}')

        self.invoke(result, "addItem", {'value': self.action.run_args[i], 'tag': i})

    @pyqtSlot(int)
    def deleteArg(self, index):
        root = self.main_controller.engine.rootObjects()
        root = root[0]
        result = root.findChild(QAbstractListModel, "listmodelargs")
        self.invoke(result, "clearItems", None)

        self.action.run_args: list = list(self.action.run_args)
        self.action.run_args.pop(index)

        self.load_page(action=self.action)


def print_child(obj, i=0):
    print('-' * 4 * i, obj.property("objectName"), obj)
    for dp in QObject.dynamicPropertyNames(obj):
        print('-' * 4 * i, 'prop:', dp, obj.property(dp))

    for c in obj.children():
        print_child(c, i + 1)
