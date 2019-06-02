from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt, QAbstractListModel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget  # pylint: disable=no-name-in-module
from .EditEventController import EditEventController  # pylint: disable=relative-beyond-top-level
from .. import GuiController, primary_color  # pylint: disable=relative-beyond-top-level

import eeve  # pylint: disable=import-error


class EventsController(GuiController):
    def load_page(self):
        root = self.main_controller.engine.rootObjects()[0]
        result = root.findChild(QAbstractListModel, "listmodel")
        for i, event in enumerate(eeve.events):
            value = {"name": event.name, "colorCode": primary_color, 'tag': i}
            self.invoke(result, 'addItem', value)

    @pyqtSlot()
    def addEvent(self):
        self.load_controller(EditEventController)

    @pyqtSlot(QObject, int, int)
    def clickedEvent(self, r, index, data):
        print('selected event:', eeve.events[data])
        r.setProperty('color', '#ff0000')
        self.load_controller(EditEventController, eeve.events[data])