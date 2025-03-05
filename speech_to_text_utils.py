import os
import io
import whisper
import ffmpeg
import torchaudio

def extract_audio(video_path, audio_path):
    """
    Extracts the audio from a video file, resamples it to 16000 Hz, and saves it as a WAV file.

    Args:
        video_path (str): Path to the input video file.
        audio_path (str): Path to save the extracted and resampled audio file.
    """

    out, _ = (
        ffmpeg
        .input(video_path)
        .output('pipe:', format='wav')
        .run(capture_stdout=True, capture_stderr=True)
    )

    signal, fs = torchaudio.load(io.BytesIO(out))
    target_fs = 16000

    if fs != target_fs:
        resampler = torchaudio.transforms.Resample(orig_freq=fs, new_freq=target_fs)
        signal = resampler(signal)

    if signal.size(0) == 2:  # If stereo convert to mono
        signal = signal.mean(dim=0, keepdim=True)

    torchaudio.save(audio_path, signal, target_fs)

def transcribe_audio(audio_path, whisper_model):
    """
    Transcribes the audio from the given file using the provided Whisper model.

    Args:
        audio_path (str): Path to the audio file to be transcribed.
        whisper_model: Preloaded Whisper model instance used for transcription.

    Returns:
        str: The transcribed text from the audio file.
    """
    result = whisper_model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    VIDEO_PATH = "Tanzania-2.mp4"
    AUDIO_PATH = "output_audio.wav"
    extract_audio(VIDEO_PATH, AUDIO_PATH)
    print(f"Audio extracted and resampled to {AUDIO_PATH}")
    audio_path = "output_audio.wav"   
    whisper_model = whisper.load_model("small")
    original_transcription = transcribe_audio(audio_path, whisper_model)
    print(original_transcription)
