from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt, QAbstractListModel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget  # pylint: disable=no-name-in-module
from .EditEventController import EditEventController  # pylint: disable=relative-beyond-top-level
from .. import GuiController, primary_color  # pylint: disable=relative-beyond-top-level

import eeve  # pylint: disable=import-error
import os
import travel_backpack
from eeve.base_classes import Event, Trigger, Action, Task  # pylint: disable=import-error


class EventsController(GuiController):
    def load_page(self):
        root = self.main_controller.engine.rootObjects()[0]
        result = root.findChild(QAbstractListModel, "listmodel")
        self.invoke(result, 'clearItems', None)
        for i, event in enumerate(eeve.events):
            value = {"name": event.name, "colorCode": primary_color, 'tag': i, 'isEventEnabled': event.enabled}
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
        eeve.events[data].enabled = False
        self.load_controller(EditEventController, eeve.events[data])

    @pyqtSlot(int)
    def deleteEvent(self, i):
        deleted_event = eeve.events.pop(i)
        deleted_event.unregister()
        self.load_page()

    @pyqtSlot(int, bool)
    def eventStateChanged(self, index, value):
        eeve.events[index].enabled = value

    def regain_focus(self, event: Event):
        print('event updated')
        event.reinitialize_triggers()
        event.enabled = True
        self.load_page()

    @pyqtSlot()
    def importFile(self):
        from ..Views import FileDialog  # pylint: disable=relative-beyond-top-level
        filedialog = FileDialog.openFileNamesDialog()

        destination_path = os.path.join(eeve.script_root, 'eeve plugins')

        for file_name in filedialog:
            travel_backpack.copy(file_name, destination_path, is_file=False)


        eeve.load_triggers_from_path(destination_path)
        eeve.load_actions_from_path(destination_path)
        print()