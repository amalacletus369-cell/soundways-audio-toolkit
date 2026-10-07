import argparse
import math
import struct
import wave
from pathlib import Path


def calculate_levels(data, sample_width):
    """Calculate peak and RMS levels from PCM audio data."""

    if sample_width == 1:
        samples = [sample - 128 for sample in data]
        max_value = 127

    elif sample_width == 2:
        count = len(data) // 2
        samples = struct.unpack(f"<{count}h", data)
        max_value = 32767

    elif sample_width == 4:
        count = len(data) // 4
        samples = struct.unpack(f"<{count}i", data)
        max_value = 2147483647

    else:
        return None, None

    if not samples:
        return 0.0, 0.0

    peak = max(abs(sample) for sample in samples)
    rms = math.sqrt(sum(sample * sample for sample in samples) / len(samples))

    peak_percent = (peak / max_value) * 100
    rms_percent = (rms / max_value) * 100

    return peak_percent, rms_percent


def analyze_audio(file_path):
    path = Path(file_path)

    if not path.exists():
        print(f"Error: '{file_path}' was not found.")
        return

    if path.suffix.lower() != ".wav":
        print("Currently, SoundWays Audio Toolkit supports WAV files.")
        return

    try:
        with wave.open(str(path), "rb") as audio:
            channels = audio.getnchannels()
            sample_rate = audio.getframerate()
            sample_width = audio.getsampwidth()
            frames = audio.getnframes()

            duration = frames / float(sample_rate)
            audio_data = audio.readframes(frames)

            peak, rms = calculate_levels(audio_data, sample_width)

            print("\n🎵 SoundWays Audio Analysis")
            print("=" * 34)
            print(f"File:        {path.name}")
            print(f"Duration:    {duration:.2f} seconds")
            print(f"Sample rate: {sample_rate} Hz")
            print(f"Channels:    {channels}")
            print(f"Bit depth:   {sample_width * 8}-bit")

            if peak is not None:
                print(f"Peak level:  {peak:.2f}%")
                print(f"RMS level:   {rms:.2f}%")
            else:
                print("Levels:      Unsupported bit depth")

            print("=" * 34)

    except wave.Error:
        print("Error: The file could not be read as a valid WAV file.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze the basic properties and levels of a WAV audio file."
    )

    parser.add_argument(
        "file",
        help="Path to the WAV file to analyze"
    )

    args = parser.parse_args()
    analyze_audio(args.file)
