from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QAbstractListModel  # pylint: disable=no-name-in-module

import eeve
from eeve.base_classes import Event, Trigger, Task, Action
from .. import GuiController  # pylint: disable=relative-beyond-top-level


class EditTriggerController(GuiController):
    def load_page(self, trigger: Trigger = None):

        self.trigger = trigger
        if self.trigger is None:
            self.trigger = Trigger.make(template=eeve.trigger_templates['on eeve startup'])

        root = self.main_controller.engine.rootObjects()
        root = root[0]
        result = root.findChild(QAbstractListModel, "tlm")
        index = 0
        for i, trigger_name in enumerate(eeve.trigger_templates):
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
        return self.trigger

    @pyqtSlot(str)
    def triggerChanged(self, trigger_name):
        self.trigger = Trigger.make(*self.trigger.args,
                                    template=eeve.trigger_templates[trigger_name],
                                    **self.trigger.kwargs)
        print(self.trigger)

    @pyqtSlot(int, str)
    def argsChanged(self, index, value):
        print(index, value)
        self.trigger.args = list(self.trigger.args)
        self.trigger.args[index] = value

    @pyqtSlot()
    def addTriggerArgument(self):
        root = self.main_controller.engine.rootObjects()
        root = root[0]
        result = root.findChild(QAbstractListModel, "listmodelargs")

        i = len(self.trigger.args)
        self.trigger.args = list(self.trigger.args)
        self.trigger.args.append(f'arg {i}')

        self.invoke(result, "addItem", {'value': self.trigger.args[i], 'tag': i})

    @pyqtSlot(int)
    def deleteArg(self, index):
        root = self.main_controller.engine.rootObjects()
        root = root[0]
        result = root.findChild(QAbstractListModel, "listmodelargs")
        self.invoke(result, "clearItems", None)

        self.trigger.args: list = list(self.trigger.args)
        self.trigger.args.pop(index)

        self.load_page(trigger=self.trigger)


def print_child(obj, i=0):
    print('-' * 4 * i, obj.property("objectName"), obj)
    for dp in QObject.dynamicPropertyNames(obj):
        print('-' * 4 * i, 'prop:', dp, obj.property(dp))

    for c in obj.children():
        print_child(c, i + 1)
