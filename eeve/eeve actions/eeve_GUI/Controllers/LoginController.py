from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget, QMessageBox  # pylint: disable=no-name-in-module
from .EventsController import EventsController
from .. import GuiController

from eeve import database


class LoginController(GuiController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @pyqtSlot(str, str)
    def login(self, user_name: str, password: str) -> None:
        try:
            print(user_name, password)
            session = database.Session()
            u = session.query(database.User).filter(database.User.login == user_name).filter(
                database.User.password == password).one()
            if u:
                self.load_controller(EventsController)
        except:
            result = QMessageBox.warning(None, 'Aviso', 'Os dados inseridos estão incorretos.')
