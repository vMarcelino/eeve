# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QMetaObject, Q_ARG, QVariant
print('importing style')
import style
print('done importing style')


class Controller(QObject):
    def __init__(self, engine: QQmlApplicationEngine):
        self.engine = engine
        QObject.__init__(self)

    viewChanged = pyqtSignal(str, arguments=['viewName'])
    eventAdded = pyqtSignal()

    @pyqtSlot(str, str)
    def login(self, user_name: str, password: str) -> None:
        self.viewChanged.emit("Events.qml")
        print(user_name, password)

    @pyqtSlot()
    def addEvent(self):
        results = self.engine.rootObjects()[0].findChild(QObject, 'batata')
        value = {"name": "batata", "colorCode": "#DDA8DD"}
        invoke(results, 'apendous', value)
        print(results)
        #self.eventAdded.emit()
        print('Added event')

    @pyqtSlot(QObject)
    def clickedEvent(self, r):
        print('did sth', r)
        r.setProperty('color', '#ff0000')


def invoke(obj, func_name: str, value):
    QMetaObject.invokeMethod(obj, func_name, Q_ARG(QVariant, value))

def main():
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    controller = Controller(engine)
    engine.rootContext().setContextProperty("controller", controller)
    engine.load("main.qml")

    engine.quit.connect(app.quit)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()