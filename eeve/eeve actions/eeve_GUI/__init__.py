# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QMetaObject, Q_ARG, QVariant, QAbstractListModel, QModelIndex
from PyQt5.QtWidgets import QListView
from . import style

import os
base_path = os.path.dirname(__file__)

import eeve
from eeve.base_classes import Event, Trigger, Task, Action

primary_color = "#666666"


class Controller(QObject):

    viewChanged = pyqtSignal(str, arguments=['viewName'])
    eventAdded = pyqtSignal()

    def __init__(self, engine: QQmlApplicationEngine):
        self.engine = engine
        QObject.__init__(self)

    @pyqtSlot(str, str)
    def login(self, user_name: str, password: str) -> None:
        print(user_name, password)
        if user_name == 'batatata' and password == 'bananinha' or True:
            self.load_events_page()

    def load_events_page(self):
        self.viewChanged.emit("Events.qml")
        root = self.engine.rootObjects()[0]
        #result = root.findChild(QObject, "listview")
        result = root.findChild(QAbstractListModel, "listmodel")
        for i, event in enumerate(eeve.events):
            value = {"name": event.name, "colorCode": primary_color, 'tag': i}
            invoke(result, 'addItem', value)

    def load_edit_event_page(self, event: Event = None):
        self.viewChanged.emit("EditEvent.qml")
        if event is None:
            event = Event(
                triggers=[Trigger.make(template=eeve.trigger_templates['on eeve startup'])],
                task=Task([Action('notepad', action_info=eeve.action_templates['run'])]),
                name='Novo evento')

        self.selected_event = event
        root = self.engine.rootObjects()[0]
        result = root.findChild(QAbstractListModel, "listmodeltriggers")
        for i, trigger in enumerate(event.triggers):
            value = {"name": trigger.name, "colorCode": primary_color, "tag": i}
            invoke(result, 'addItem', value)

        result = root.findChild(QAbstractListModel, "listmodelactions")
        for i, action in enumerate(event.task.actions):
            value = {"name": action.name, "colorCode": primary_color, "tag": i}
            invoke(result, 'addItem', value)

    def load_edit_trigger_page(self, trigger: Trigger = None):
        self.viewChanged.emit("EditTrigger.qml")
        if trigger is None:
            trigger = Trigger.make(template=eeve.trigger_templates['on eeve startup'])

    @pyqtSlot()
    def addEvent(self):
        self.load_edit_event_page()

    @pyqtSlot(QObject, int, int)
    def clickedEvent(self, r, index, data):
        print('selected event:', eeve.events[data])
        r.setProperty('color', '#ff0000')
        self.load_edit_event_page(eeve.events[data])

    @pyqtSlot(QObject, int, int)
    def clickedTrigger(self, r, index, data):
        print('selected trigger:', self.selected_event.triggers[data])
        r.setProperty('color', '#ff0000')
        self.load_edit_trigger_page(self.selected_event.triggers[data])

    @pyqtSlot()
    def addTrigger(self):
        print('add trigger')
        self.load_edit_trigger_page()

    @pyqtSlot()
    def addAction(self):
        print('add action')
        root = self.engine.rootObjects()[0]
        result = root.findChild(QAbstractListModel, "listmodelactions")
        value = {"name": "asd", "colorCode": primary_color}
        invoke(result, 'addItem', value)


def invoke(obj, func_name: str, value):
    return QMetaObject.invokeMethod(obj, func_name, Q_ARG(QVariant, value))


def main():
    try:
        print('Starting GUI')
        app = QGuiApplication(sys.argv)

        engine = QQmlApplicationEngine()
        controller = Controller(engine)
        engine.rootContext().setContextProperty("controller", controller)

        engine.load(os.path.join(base_path, "main.qml"))

        def hide_all():
            print('hiding all root objects')
            for r in engine.rootObjects():
                r.hide()

        engine.quit.connect(hide_all)
        #engine.quit.connect(app.quit)
        app.exec_()
        print('application ended')
        app = None

    except Exception as ex:
        print(ex)
        pass


if __name__ == "__main__":
    main()

actions = {"start gui": {'run': main}}
