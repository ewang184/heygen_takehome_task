import subprocess
import argparse

def run_shell_scripts_and_python(video_file):
    print("Running translation...")
    subprocess.run(f"echo {video_file} | ./run_translate.sh", check=True, shell=True)

    print("Running re-synthesis...")
    subprocess.run(["./run_hift.sh"], check=True, shell=True)

    print("Running audio replacement...")
    subprocess.run(["python", "replace_audio.py"], check=True)

    print("Running lipsync...")
    subprocess.run(f"echo {video_file} | ./run_musetalk.sh", check=True, shell=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Run video translation with a given file.")
    parser.add_argument("video_file", type=str, help="Path to the video file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    video_file = args.video_file
    run_shell_scripts_and_python(video_file)

