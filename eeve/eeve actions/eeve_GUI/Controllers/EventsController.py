from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt, QAbstractListModel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget  # pylint: disable=no-name-in-module
from .EditEventController import EditEventController  # pylint: disable=relative-beyond-top-level
from .. import GuiController, primary_color  # pylint: disable=relative-beyond-top-level

import eeve  # pylint: disable=import-error
from eeve.base_classes import Event, Trigger, Action, Task  # pylint: disable=import-error


class EventsController(GuiController):
    def load_page(self):
        root = self.main_controller.engine.rootObjects()[0]
        result = root.findChild(QAbstractListModel, "listmodel")
        self.invoke(result, 'clearItems', None)
        for i, event in enumerate(eeve.events):
            value = {"name": event.name, "colorCode": primary_color, 'tag': i}
            self.invoke(result, 'addItem', value)

    @pyqtSlot()
    def addEvent(self):
        event = Event(triggers=[Trigger.make(template=eeve.trigger_templates['on eeve startup'])],
                      task=Task([Action('notepad', action_info=eeve.action_templates['run'])]),
                      name='Novo evento',
                      enabled=False)
        eeve.events.append(event)
        self.load_controller(EditEventController, event)

    @pyqtSlot(QObject, int, int)
    def clickedEvent(self, r, index, data):
        #print('selected event:', eeve.events[data])
        r.setProperty('color', '#ff0000')
        self.load_controller(EditEventController, eeve.events[data])

    @pyqtSlot(int)
    def deleteEvent(self, i):
        eeve.events.pop(i)
        self.load_page()

    def regain_focus(self, event: Event):
        event.reinitialize_triggers()
        event.enabled = True
        self.load_page()