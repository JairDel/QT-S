from PyQt5 import QtWidgets
from ventana_ui import Ui_MainWindow
from python_event_bus import EventBus
from threading import Thread
import uvicorn
import main

#print(f"ID del EventBus en ventana.py: {id(EventBus)}")


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.label.setText("Haz clic en el botón")
        self.pushButton.setText("Presióname")
        self.pushButton.clicked.connect(self.actualizar)

        #EventBus.subscribe("new_cli", self.nuevo_cliente)
        #EventBus.subscribe("cli_say", self.mostrar_mensaje)

    def actualizar(self):
        self.label.setText("¡Acabas de hacer clic en el botón!")
        EventBus.call("QT5_say", "Botón presionado")

    @EventBus.on("websocket_say")
    def WSConnect(message):
        global window
        window.label.setText(message)

def run_fastapi():
    config = uvicorn.Config(main.app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    server.run()

def QT():
    global window
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    fastapi_thread = Thread(target=run_fastapi)
    fastapi_thread.start()
    QT()
    fastapi_thread.join()
