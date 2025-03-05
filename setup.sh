#!/bin/bash

# Step 1: Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Step 2: Create the 'warped_audio' folder if it doesn't exist
echo "Creating 'warped_audio' folder..."
mkdir -p warped_audio

# Step 3: Create the 'german_sentences' folder if it doesn't exist
echo "Creating 'german_sentences' folder..."
mkdir -p german_sentences

echo "Setup completed successfully!"

