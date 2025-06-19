import sys
from PyQt5 import QtWidgets, QtCore

from main import ArduinoBackend


class MainWindow(QtWidgets.QWidget):
    def __init__(self, port: str = "COM4", baud: int = 9600):
        super().__init__()
        self.backend = ArduinoBackend(port, baud)

        # --- UI --- #
        self.setWindowTitle("Arduino Control")
        self.resize(480, 320)

        self.output = QtWidgets.QTextEdit(readOnly=True)
        self.input = QtWidgets.QLineEdit()
        self.send_btn = QtWidgets.QPushButton("Send")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.output)
        hl = QtWidgets.QHBoxLayout()
        hl.addWidget(self.input)
        hl.addWidget(self.send_btn)
        layout.addLayout(hl)

        self.send_btn.clicked.connect(self._send_cmd)
        self.input.returnPressed.connect(self._send_cmd)

        # Timer to pump backend messages
        self.timer = QtCore.QTimer(interval=50)
        self.timer.timeout.connect(self._poll_backend)
        self.timer.start()

    # ---------------- slots ---------------- #
    def _send_cmd(self):
        cmd = self.input.text().strip()
        if cmd:
            self.backend.send(cmd)
            self.output.append(f"[PC] {cmd}")
            self.input.clear()

    def _poll_backend(self):
        line = self.backend.read()
        if line:
            self.output.append(f"[ARDUINO] {line}")

    def closeEvent(self, e):
        self.backend.close()
        super().closeEvent(e)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
