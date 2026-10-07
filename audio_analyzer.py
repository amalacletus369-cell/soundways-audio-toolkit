import argparse
import wave
from pathlib import Path
import audioop


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

            peak = audioop.max(audio_data, sample_width)
            rms = audioop.rms(audio_data, sample_width)

            max_possible = float((2 ** (8 * sample_width - 1)) - 1)

            peak_percent = (peak / max_possible) * 100
            rms_percent = (rms / max_possible) * 100

            print("\n🎵 SoundWays Audio Analysis")
            print("=" * 32)
            print(f"File:        {path.name}")
            print(f"Duration:    {duration:.2f} seconds")
            print(f"Sample rate: {sample_rate} Hz")
            print(f"Channels:    {channels}")
            print(f"Bit depth:   {sample_width * 8}-bit")
            print(f"Peak level:  {peak_percent:.2f}%")
            print(f"RMS level:   {rms_percent:.2f}%")
            print("=" * 32)

    except wave.Error:
        print("Error: The file could not be read as a valid WAV file.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze basic properties of a WAV audio file."
    )
    parser.add_argument("file", help="Path to the WAV file to analyze")

    args = parser.parse_args()
    analyze_audio(args.file)
