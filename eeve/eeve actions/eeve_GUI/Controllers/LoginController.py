from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget  # pylint: disable=no-name-in-module
from .EventsController import EventsController
from .. import GuiController


class LoginController(GuiController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @pyqtSlot(str, str)
    def login(self, user_name: str, password: str) -> None:
        print(user_name, password)
        if user_name == 'batatata' and password == 'bananinha' or True:
            self.load_controller(EventsController)
