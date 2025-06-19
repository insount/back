import serial
import threading

# Замените на нужный порт и скорость
PORT = 'COM4'       # или '/dev/ttyUSB0' на Linux/Mac
BAUD = 9600

# Открытие порта
ser = serial.Serial(PORT, BAUD, timeout=1)

# Функция для чтения из Arduino в отдельном потоке
def read_from_arduino():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"[ARDUINO] {line}")

# Запуск потока чтения
threading.Thread(target=read_from_arduino, daemon=True).start()

# Главный цикл для ввода команд
print("Введите команду (например, JUSTIFY, SPIN, MOVE, stop, ANG:90 SPD:100 DIR:1):")

while True:
    try:
        cmd = input(">> ").strip()
        if cmd:
            ser.write((cmd + '\n').encode('utf-8'))
    except KeyboardInterrupt:
        print("\nВыход...")
        break
