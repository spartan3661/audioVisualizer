from PyQt5.QtCore import QThread, pyqtSignal
import soundcard as sc
import numpy as np


class AudioProcessor(QThread):
    new_frequency_data = pyqtSignal(np.ndarray)

    def run(self):
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(
                samplerate=44100) as mic:
            while True:
                chunk = mic.record(numframes=1024)
                chunk = chunk[:, 0]
                chunk = chunk.astype(np.float32)
                fft_result = np.fft.fft(chunk)
                frequencies = np.abs(fft_result)[:700]

                # Dampen bass frequencies
                bass_dampen = np.linspace(0.5, 1.0, len(frequencies) // 4)

                # Boost treble frequencies
                treble_boost = np.linspace(1.0, 3.0, len(frequencies) // 4)

                # Boost brilliance frequencies
                brilliance_boost = np.linspace(1.0, 3.0, len(frequencies) // 4)
                brilliance_boost = np.concatenate([np.ones(len(frequencies) - len(brilliance_boost)), brilliance_boost])

                bass_dampen = np.concatenate([bass_dampen, np.ones(len(frequencies) - len(bass_dampen))])
                treble_boost = np.concatenate([np.ones(len(frequencies) - len(treble_boost)), treble_boost])

                frequencies *= bass_dampen
                frequencies *= treble_boost
                frequencies *= brilliance_boost

                # Normalize frequencies
                max_value = np.max(frequencies)
                if max_value > 0:
                    frequencies = (frequencies / max_value) * 100

                self.new_frequency_data.emit(frequencies)
