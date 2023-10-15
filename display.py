import math

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QRect
import sys
import numpy as np
from audioProcessing import AudioProcessor

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.frequencies = np.array([])

    def set_frequencies(self, frequencies):
        self.frequencies = frequencies
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        if self.frequencies.size > 0:
            bar_width = self.width() / len(self.frequencies)
            for i, f in enumerate(self.frequencies):
                # Create a QColor object with reversed smoothly changing RGB values
                r = int(127.5 * (1 - math.sin(math.pi * i / len(self.frequencies))))
                g = int(127.5 * (1 - math.cos(math.pi * i / len(self.frequencies))))
                b = int(127.5 * (1 + math.sin(math.pi * i / len(self.frequencies))))

                color = QColor(r, g, b)

                painter.setBrush(color)
                painter.drawRect(QRect(int(i * bar_width), self.height(), int(bar_width), int(-f)))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Set default size
        self.resize(800, 200)

        # Make the window non-resizable
        self.setFixedSize(800, 200)
        self.setWindowTitle("Simple Audio Visualizer")
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        self.audio_processor = AudioProcessor()
        self.audio_processor.new_frequency_data.connect(self.update_gui)  # Connect the slot to the signal
        self.audio_processor.start()
        self.setStyleSheet("background-color: black;")
    def update_gui(self, frequencies: np.ndarray):
        # Scale the frequencies to fit in the window.
        if np.all(np.isclose(frequencies, 0, atol=1e-6)):
            self.canvas.set_frequencies(np.zeros_like(frequencies))
        else:
            scaled_frequencies = np.interp(frequencies, (frequencies.min(), frequencies.max()), (0, 255))
            self.canvas.set_frequencies(scaled_frequencies)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
