import sounddevice as sd
from scipy.io.wavfile import write
import os
os.environ["FFMPEG_BINARY"] = r"C:\Users\97250\bin\ffmpeg.exe"
import whisper


def record_to_file(path: str, seconds: float = 3.0, sr: int = 16000) -> str:
    """
    Records audio from the default microphone for 'seconds' seconds
    and saves it as a WAV file at the specified 'path'.
    
    Parameters:
        path (str): The path where the WAV file will be saved.
        seconds (float): Duration of the recording in seconds (default: 3).
        sr (int): Sampling rate in Hz (default: 16000).
    
    Returns:
        str: The path to the saved WAV file.
    """
    print(f"Recording for {seconds} seconds...")
    audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="int16")
    sd.wait()  # Wait until recording is finished
    
    # Save the recorded audio to a WAV file
    write(path, sr, audio)
    print(f"Recording saved as {path}")
    return path


def transcribe(path: str, model_size: str = "base", language: str | None = None) -> str:
    """
    Transcribes an audio file using OpenAI Whisper.
    Raises clear errors if the file doesn't exist or Whisper is not installed.
    
    Parameters:
        path (str): Path to the audio file to transcribe.
        model_size (str): Size of the Whisper model ('tiny', 'base', 'small', 'medium', 'large').
        language (str | None): Language code to force transcription (e.g., 'he' for Hebrew).
    
    Returns:
        str: The transcribed text.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist! Please record or check the path.")
    
    # Check if Whisper is installed
    if whisper is None:
        raise RuntimeError("Whisper is not installed. Install it with: pip install openai-whisper")
    
    # Load the Whisper model
    model = whisper.load_model(model_size)
    
    # Transcribe the audio
    result = model.transcribe(path, language=language)
    text = result.get("text", "").strip()
    
    if not text:
        print("No text was returned from the audio – the recording may be too quiet or unclear.")
    
    return text


# Example usage
if __name__ == "__main__":
    file_path = "user_input.wav"
    
    # Record a short audio clip
    record_to_file(file_path, seconds=15)
    
    # Transcribe the recorded audio
    text = transcribe(file_path, model_size="small", language="he")
    print("Transcription:", text)
