import serial
import threading
import queue
from typing import Callable, Optional


class ArduinoBackend:
    """Serial bridge to Arduino."""

    def __init__(self, port: str, baud: int = 9600):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(port, baud, timeout=1)
        self._recv_queue: "queue.Queue[str]" = queue.Queue()
        self._running = True
        self._callbacks: list[Callable[[str], None]] = []

        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()

    # ---------------- private ---------------- #
    def _read_loop(self):
        while self._running:
            try:
                if self.ser.in_waiting:
                    line = (
                        self.ser.readline()
                        .decode("utf-8", errors="ignore")
                        .strip()
                    )
                    if line:
                        self._recv_queue.put(line)
                        for cb in self._callbacks:
                            cb(line)
            except serial.SerialException:
                break

    # ---------------- public ---------------- #
    def send(self, cmd: str):
        if not cmd.endswith("\n"):
            cmd += "\n"
        self.ser.write(cmd.encode("utf-8"))

    def read(self, timeout: float = 0.1) -> Optional[str]:
        try:
            return self._recv_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def add_callback(self, cb: Callable[[str], None]):
        self._callbacks.append(cb)

    def close(self):
        self._running = False
        self._reader.join()
        self.ser.close()
