git clone https://github.com/yl4579/HiFTNet.git

SRC_FILE="resynth.py"
DEST_DIR="HiFTNet"

if [ -f "$SRC_FILE" ]; then
    mv "$SRC_FILE" "$DEST_DIR/"
    echo "Moved $SRC_FILE to $DEST_DIR"
fi

SRC_FILE="download_cp_hifigan.py"

if [ -f "$SRC_FILE" ]; then
    mv "$SRC_FILE" "$DEST_DIR/"
    echo "Moved $SRC_FILE to $DEST_DIR"
fi

cd HiFTNet

new_requirements="torch
numpy==1.26.4
scipy==1.13.1
matplotlib==3.8.4
librosa==0.10.2.post1
soundfile==0.13.1
tensorboard==2.19.0
"

requirements_file_path='./requirements.txt'

echo "$new_requirements" > "$requirements_file_path"

echo "requirements.txt has been updated."

python3.10 -m venv hift_env

VENV_PATH="hift_env/bin/activate"

if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    echo "Virtual environment activated."
else
    echo "Error: Virtual environment activate script not found."
    exit 1
fi

pip install -r requirements.txt

python download_cp_hifigan.py

python resynth.py

cd ..
