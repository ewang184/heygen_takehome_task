from text_to_speech_utils import process_text_to_speech
from speech_to_text_utils import transcribe_audio, extract_audio
from text_translate_utils import translate_text
from speech_to_text_align import extract_special_timings, word_timings
import argparse
from transformers import MarianMTModel, MarianTokenizer
import whisper
from TTS.api import TTS

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Translate audio from a MP4 file.")
    parser.add_argument("mp4_file", type=str, help="Path to the MP4 file")

    # Parse the arguments
    args = parser.parse_args()
    mp4_file_name = args.mp4_file

    # Extract audio from mp4 to a wav file
    temp_audio_path = "temp_audio_path.wav"
    extract_audio(mp4_file_name, temp_audio_path)

    # Use whisper model to get english transcription from wav file
    whisper_model = whisper.load_model("small")
    original_transcription = transcribe_audio(temp_audio_path, whisper_model)

    # Use Helsinki-NLP model to translate transcription to german
    src_lang = "en"
    tgt_lang = "de"
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    translated_text = translate_text(original_transcription, model, tokenizer)

    # Calculate sentence timings
    timings = word_timings(original_transcription, "temp_audio_path.wav")
    sentence_timings = extract_special_timings(timings)

    # Speak individual german sentences, with time warping to match english sentence length
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    process_text_to_speech(translated_text, temp_audio_path, sentence_timings, tts)

if __name__ == "__main__":
    main()
