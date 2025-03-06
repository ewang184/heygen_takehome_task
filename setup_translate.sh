#!/bin/bash

RUN python3.10 -m venv heygen_env

VENV_PATH="heygen_env/bin/activate"

if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    echo "Virtual environment activated."
else
    echo "Error: Virtual environment activate script not found."
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt
pip uninstall numpy --yes
pip install "numpy<2"

echo "Creating 'warped_audio' folder..."
mkdir -p warped_audio

echo "Creating 'german_sentences' folder..."
mkdir -p german_sentences

video_file="$1"
if [ -z "$video_file" ]; then
  echo "Error: Please provide the path to the video file as an argument."
  exit 1
fi

python translate_video.py "$video_file"
