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

video_file="$1"
if [ -z "$video_file" ]; then
  echo "Error: Please provide the path to the video file as an argument."
  exit 1
fi

python translate_video.py "$video_file"

deactivate
