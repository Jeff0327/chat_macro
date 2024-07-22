import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox
from PyQt5.QtCore import QThread, pyqtSignal
import ctypes

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def press_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def release_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def macro_chat():
    # Enter
    press_key(0x1C)
    time.sleep(0.1)
    release_key(0x1C)
    time.sleep(0.5)
    
    # Ctrl+V
    press_key(0x1D)  # Ctrl
    press_key(0x2F)  # V
    time.sleep(0.1)
    release_key(0x2F)
    release_key(0x1D)
    time.sleep(0.5)
    
    # Enter
    press_key(0x1C)
    time.sleep(0.1)
    release_key(0x1C)
class MacroThread(QThread):
    update_signal = pyqtSignal(str)
    countdown_signal = pyqtSignal(int)

    def __init__(self, interval):
        QThread.__init__(self)
        self.interval = interval
        self.is_running = True

    def run(self):
        self.update_signal.emit("매크로 시작 준비 중... 5초 후 시작됩니다.")
        for i in range(5, 0, -1):
            self.countdown_signal.emit(i)
            time.sleep(1)
        
        while self.is_running:
            self.update_signal.emit("매크로 실행 중...")
            macro_chat()
            self.update_signal.emit(f"다음 실행까지 {self.interval}초 대기")
            for i in range(self.interval, 0, -1):
                if not self.is_running:
                    break
                self.countdown_signal.emit(i)
                time.sleep(1)

    def stop(self):
        self.is_running = False

class MacroUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.macro_thread = None

    def initUI(self):
        self.setWindowTitle('매크로 프로그램')
        
        layout = QVBoxLayout()

        self.status_label = QLabel('준비됨', self)
        layout.addWidget(self.status_label)

        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel('실행 간격(초):'))
        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setRange(1, 3600)
        self.interval_spinbox.setValue(10)
        interval_layout.addWidget(self.interval_spinbox)
        layout.addLayout(interval_layout)

        self.delay_label = QLabel('현재 딜레이: 10초', self)
        layout.addWidget(self.delay_label)

        self.countdown_label = QLabel('', self)
        layout.addWidget(self.countdown_label)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton('시작', self)
        self.start_button.clicked.connect(self.start_macro)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton('중지', self)
        self.stop_button.clicked.connect(self.stop_macro)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def start_macro(self):
        interval = self.interval_spinbox.value()
        self.delay_label.setText(f'현재 딜레이: {interval}초')
        self.macro_thread = MacroThread(interval)
        self.macro_thread.update_signal.connect(self.update_status)
        self.macro_thread.countdown_signal.connect(self.update_countdown)
        self.macro_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_macro(self):
        if self.macro_thread:
            self.macro_thread.stop()
            self.macro_thread.wait()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText('매크로 중지됨')
        self.countdown_label.setText('')

    def update_status(self, message):
        self.status_label.setText(message)

    def update_countdown(self, seconds):
        self.countdown_label.setText(f'남은 시간: {seconds}초')

    def closeEvent(self, event):
        self.stop_macro()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MacroUI()
    sys.exit(app.exec_())