import tempfile
import unittest
import wave
from pathlib import Path

from audio_analyzer import calculate_levels


class TestAudioAnalyzer(unittest.TestCase):

    def test_silence_has_zero_levels(self):
        data = b"\x00\x00" * 100

        peak, rms = calculate_levels(data, 2)

        self.assertEqual(peak, 0.0)
        self.assertEqual(rms, 0.0)

    def test_unsupported_bit_depth(self):
        data = b"\x00" * 100

        peak, rms = calculate_levels(data, 3)

        self.assertIsNone(peak)
        self.assertIsNone(rms)

    def test_create_valid_wav(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.wav"

            with wave.open(str(path), "wb") as audio:
                audio.setnchannels(1)
                audio.setsampwidth(2)
                audio.setframerate(44100)
                audio.writeframes(b"\x00\x00" * 44100)

            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
