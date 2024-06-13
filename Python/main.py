from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice

# By default, for Servos like MG996R the range 0-180 is set,
# well if something will interfere with the servo rotation -
# it is very bad, so you will need to calibrate the range of
# rotation manually.
# This must be done in the function set_range_servo


class SerialCommunicationApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("design.ui", self)     # design.ui - file Qt Design
        self.connected = False
        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)
        self.com_ports()
        self.setup_connections()
        self.set_range_servo()
        self.update_servo_state()

    def com_ports(self):
        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            self.ui.listComPorts.addItem(port.portName())

    def set_range_servo(self):
        self.ui.servo0.setMinimum(24)
        self.ui.servo0.setMaximum(97)
        self.ui.servo1.setMinimum(0)
        self.ui.servo1.setMaximum(180)
        self.ui.servo2.setMinimum(0)
        self.ui.servo2.setMaximum(180)
        self.ui.servo3.setMinimum(0)
        self.ui.servo3.setMaximum(180)
        self.ui.servo4.setMinimum(0)
        self.ui.servo4.setMaximum(180)
        self.ui.servo5.setMinimum(0)
        self.ui.servo5.setMaximum(180)

    def setup_connections(self):
        self.ui.btnOpenComPort.clicked.connect(self.open_com_port)
        self.ui.btnCloseComPort.clicked.connect(self.close_com_port)
        self.ui.servo0.valueChanged.connect(lambda val: self.on_servo(val, 0))
        self.ui.servo1.valueChanged.connect(lambda val: self.on_servo(val, 1))
        self.ui.servo2.valueChanged.connect(lambda val: self.on_servo(val, 2))
        self.ui.servo3.valueChanged.connect(lambda val: self.on_servo(val, 3))
        self.ui.servo4.valueChanged.connect(lambda val: self.on_servo(val, 4))
        self.ui.servo5.valueChanged.connect(lambda val: self.on_servo(val, 5))

    def open_com_port(self):
        self.serial.setPortName(self.ui.listComPorts.currentText())
        if self.serial.open(QIODevice.ReadWrite):
            self.connected = True
            print(f"Opened {self.ui.listComPorts.currentText()}")
        else:
            self.connected = False
            print(f"Failed to open {self.ui.listComPorts.currentText()}")
        self.update_servo_state()

    def close_com_port(self):
        if self.serial.isOpen():
            self.serial.close()
            self.connected = False
            print("COM port Arduino: closed")
        self.update_servo_state()

    def on_servo(self, val, num_engine):
        output_data = f"{num_engine}:{val}\n"
        self.serial.write(output_data.encode())
        # print(output_data)

    def update_servo_state(self):
        self.servo0.setEnabled(self.connected)
        self.servo1.setEnabled(self.connected)
        self.servo2.setEnabled(self.connected)
        self.servo3.setEnabled(self.connected)
        self.servo4.setEnabled(self.connected)
        self.servo5.setEnabled(self.connected)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = SerialCommunicationApp()
    window.show()
    app.aboutToQuit.connect(window.close_com_port)
    app.exec()
