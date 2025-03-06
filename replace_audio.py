import moviepy.editor as mp
import os

def replace_audio(video_input, audio_input, output_video):
    """
    Replace the audio of a video with a new audio file.

    Args:
        video_input (str): Path to the input video file.
        audio_input (str): Path to the input audio (WAV) file.
        output_video (str): Path to save the output video with replaced audio.
    """
    if not os.path.isfile(video_input):
        raise FileNotFoundError(f"Video file not found: {video_input}")

    if not os.path.isfile(audio_input):
        raise FileNotFoundError(f"Audio file not found: {audio_input}")

    try:
        video = mp.VideoFileClip(video_input)
        audio = mp.AudioFileClip(audio_input)
        video = video.set_audio(audio)
        video.write_videofile(output_video, codec='libx264', audio_codec='aac')
        print(f"Audio replaced successfully. Output saved to {output_video}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    video_path = "Tanzania-2.mp4"
    audio_path = "output_resynthesized.wav"
    output_path = "Translated_German_Tanzania.mp4"

    replace_audio(video_path, audio_path, output_path)

