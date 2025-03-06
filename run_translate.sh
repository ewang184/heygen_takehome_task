#!/bin/bash

python3.10 -m venv heygen_env

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

echo "Creating 'warped_audio' folder..."
mkdir -p warped_audio

echo "Creating 'german_sentences' folder..."
mkdir -p german_sentences

echo "Enter the path to the video file (e.g., Tanzania-2.mp4):"
read video_file

python translate_video.py "$video_file"

pip uninstall numpy --yes
pip install "numpy<2"

python time_video.py translated_text.txt

source deactivate

