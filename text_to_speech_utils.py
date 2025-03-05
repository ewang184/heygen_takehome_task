import os
from pydub import AudioSegment
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from tqdm import tqdm
import librosa
import soundfile as sf

def warp_audio(input_path, output_path, target_duration):
    """
    Time-stretches an audio file to match a target duration and saves the modified audio.

    This function loads an audio file, calculates the stretch factor needed to adjust its duration
    to the specified target duration, applies time-stretching using Librosa, and saves the
    resulting audio to a new file.

    Args:
        input_path (str): Path to the input audio file.
        output_path (str): Path to save the time-stretched audio file.
        target_duration (float): Desired duration of the output audio in seconds.

    Returns:
        None
    """
    y, sr = librosa.load(input_path, sr=None)
    y = y.astype('float32')
    current_duration = librosa.get_duration(y=y, sr=sr)
    stretch_factor = current_duration / target_duration
    try:
        y_stretched = librosa.effects.time_stretch(y, rate=stretch_factor)
    except Exception as e:
        print(f"Error during time stretching: {e}")
        print(f"y dtype: {y.dtype}, y shape: {y.shape}, sr: {sr}, stretch factor: {stretch_factor}")
        raise
    sf.write(output_path, y_stretched, sr)

def process_text(text):
    """
    Processes a string into a list of sentences.

    This function takes as input a text string, removes newlines, and then splits the text
    into sentences, splitting on periods.
    
    Args:
        text (str): Input string to process

    Returns:
        list[str] A list of sentences in the original texxt
    """

    cleaned_text = text.replace("\n", " ").replace("\r", " ").strip()
    sentences = [sentence.strip() for sentence in cleaned_text.split(".") if sentence.strip()]
    return sentences


def combine_wavs_from_directory(directory, output_file):
    """
    Combines all WAV files in a directory into a single audio file with short silences between them.

    This function gathers all .wav files from the specified directory, sorts them, and combines them
    into a single audio file with 200ms of silence between each file. The combined audio is saved
    as a new WAV file.

    Args:
        directory (str): Path to the directory containing the .wav files.
        output_file (str): Path to save the combined audio file.

    Returns:
        None
    """

    combined = AudioSegment.empty()

    wav_files = [f for f in os.listdir(directory) if f.endswith('.wav')]
    wav_files.sort()

    for i,wav_file in enumerate(wav_files):
        wav_path = os.path.join(directory, wav_file)
        audio = AudioSegment.from_wav(wav_path)

        if i > 0:
            silence = AudioSegment.silent(duration=200)  # Create silence of the specified duration
            combined += silence

        combined += audio

    combined.export(output_file, format="wav")
    print(f"Combined audio saved to {output_file}")

def get_difference(times):
    """
    Calculates the differences between consecutive time values, including the difference from zero.

    This function takes a list of time values and computes the difference between each value and
    its predecessor, with the first difference calculated from an assumed initial value of zero.

    Args:
        times (list[float]): A list of time values (e.g., timestamps in seconds).

    Returns:
        list[float]: A list of differences between consecutive time values.
    """

    values = [0]+times
    differences = [values[i] - values[i - 1] for i in range(1, len(values))]
    return differences

def combine_wavs_given_time(directory, output_file, times):
    """
    Combines and time-stretches WAV files from a directory based on specified time durations.

    This function takes a list of times, applies time-stretching to each corresponding WAV file
    in the directory, and then combines the warped audio files into a single output file. The
    WAV files are processed in the order they appear in the directory.

    Args:
        directory (str): Path to the directory containing the original .wav files.
        output_file (str): Path to save the final combined and time-stretched audio file.
        times (list[float]): A list of target durations for each corresponding WAV file.

    Returns:
        None
    """

    differences = get_difference(times)
    wav_files = [f for f in os.listdir(directory) if f.endswith('.wav')]
    wav_files.sort()
    for i,time in enumerate(differences):
        warp_audio(os.path.join("german_sentences", wav_files[i]), f"./warped_audio/{i}warped.wav", target_duration=time)        

    combine_wavs_from_directory("warped_audio", output_file)

def process_text_to_speech(text, wav_name, sentence_times, tts):
    sentences = process_text(text)
    for i, sentence in tqdm(enumerate(sentences), total=len(sentences), desc="Generating Speech"):
        tts.tts_to_file(text=sentence,
                        file_path=f"german_sentences/{i}german.wav",
                        speaker_wav=wav_name,
                        language="de")

    combine_wavs_given_time('german_sentences', 'warped_german_voice.wav', sentence_times)

if __name__ == "__main__":
    text = """Tansania, die Heimat einiger der atemberaubendsten Tierwelten der Erde.
    Hier im Herzen Ostafrikas, beherbergt der große Serengeti-Nationalpark eines der größten Spektakel der Natur, die Große Migration. Über eine Million Wildebeest, Zebras und Gazellen reisen weite Strecken auf der Suche nach frischem Gras, glühende Flüsse voller Krokodile.
    Aber Raubtiere sind nie weit dahinter. Löwen, die Könige der Savanne, verfolgen ihre Beute mit Geduld und Präzision.
    Cheetahs, die schnellsten Landtiere, jagen ihre Ziele in einer spannenden Schau der Geschwindigkeit.
    Im üppigen Terengair-Nationalpark streifen riesige Elefanten frei umher.
    Diese intelligenten Kreaturen bilden starke Familienbande, die ihre Jungen vor Bedrohungen schützen.
    Und im alten Krater Ngorongoro findet der gefährdete schwarze Nashorn Zuflucht, ein seltener Anblick in der Wildnis.
    Tansanias Wildtiere sind ein Schatz wie kein anderer, ein zartes Gleichgewicht der Natur, das uns an die Schönheit und Kraft der Wildnis erinnert.
    """

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

    sentences = process_text(text)

    for i, sentence in tqdm(enumerate(sentences), total=len(sentences), desc="Generating Speech"):
        tts.tts_to_file(text=sentence,
                        file_path=f"german_sentences/{i}german.wav",
                        speaker_wav="temp_audio_path.wav",
                        language="de")

    sentence_times = [4.0411875, 12.3438125, 21.8066875, 24.6275625, 29.689125, 35.370875, 39.9323125, 44.7538125, 51.7159375, 59.8184375]

    combine_wavs_given_time('german_sentences', 'warped_german_voice.wav', sentence_times)
