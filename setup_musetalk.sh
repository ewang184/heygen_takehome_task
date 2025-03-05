git clone https://github.com/TMElyralab/MuseTalk.git

SRC_FILE="download_requirements.py"
DEST_DIR="HiFTNet"

if [ -f "$SRC_FILE" ]; then
    mv "$SRC_FILE" "$DEST_DIR/"
    echo "Moved $SRC_FILE to $DEST_DIR"
fi

SRC_FILE="setup_folders.py"

if [ -f "$SRC_FILE" ]; then
    mv "$SRC_FILE" "$DEST_DIR/"
    echo "Moved $SRC_FILE to $DEST_DIR"
fi

cd MuseTalk

python3.10 -m venv muse_env

VENV_PATH="muse_env/bin/activate"

if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    echo "Virtual environment activated."

else
    echo "Error: Virtual environment activate script not found."
    exit 1
fi

pip install -r requirements.txt
pip install --no-cache-dir -U openmim 
mim install mmengine 
mim install "mmcv>=2.0.1" 
mim install "mmdet>=3.1.0" 
mim install "mmpose>=1.1.0" 

python setup_folders.py
python download_requirements.py

./musetalk_ffmpeg.sh 

source deactivate

cd ..
