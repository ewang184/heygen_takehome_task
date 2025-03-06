#!/bin/bash

echo "Creating 'warped_audio' folder..."
mkdir -p warped_audio

echo "Creating 'german_sentences' folder..."
mkdir -p german_sentences

python install_espeak.py 

echo "Setup completed successfully!"

