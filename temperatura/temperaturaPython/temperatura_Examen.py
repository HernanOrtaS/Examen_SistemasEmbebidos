import sys
import serial as conecta
from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile = "temperatura_Examen.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

iluminacion_minima = 0

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Área de los Signals
        self.txt_puerto.setText("COM3")

        self.btn_accion.clicked.connect(self.accion)
        self.arduino = None

        self.segundoPlano = QtCore.QTimer()
        self.segundoPlano.timeout.connect(self.control)

        self.btn_guardar.clicked.connect(self.guardar)
        # self.btn_control_led.setEnabled(False)

        self.cont = 1

    # Área de los Slots
    def guardar(self):
        global iluminacion_minima
        iluminacion_minima = self.spinBox.value()
        self.txt_calibrar.setText(f"Luz Min: {iluminacion_minima}")

    def accion(self):  # conecta/desconecta/reconecta vinculo con arduino
        try:
            txt_btn = self.btn_accion.text()
            if txt_btn == "CONECTAR":  # arduino == None
                puerto = self.txt_puerto.text()
                self.arduino = conecta.Serial(puerto, baudrate=9600, timeout=1)
                self.segundoPlano.start(1000)  # Leer datos cada 1000ms (1 segundo)
                self.txt_estado.setText("CONECTADO")
                self.btn_accion.setText("DESCONECTAR")

            elif txt_btn == "DESCONECTAR":
                if self.arduino and self.arduino.isOpen():
                    self.segundoPlano.stop()
                    self.arduino.close()
                self.txt_estado.setText("DESCONECTADO")
                self.btn_accion.setText("RECONECTAR")

            else:  # RECONECTAR
                self.arduino.open()
                self.segundoPlano.start(1000)  # Leer datos cada 1000ms (1 segundo)
                self.txt_estado.setText("RECONECTADO")
                self.btn_accion.setText("DESCONECTAR")

        except Exception as error:
            print(f"Error en la conexión: {error}")

    def control(self):
        if self.arduino is not None and self.arduino.isOpen():
            if self.arduino.inWaiting():
                cadena = self.arduino.readline().decode().strip()
                valor = (int(cadena)) - 900
                self.txt_luz.setText(f"Luz Actual: {valor}")

                print(valor, "\t", iluminacion_minima)

                if valor < iluminacion_minima:
                    self.arduino.write("11".encode())
                else:
                    self.arduino.write("12".encode())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
