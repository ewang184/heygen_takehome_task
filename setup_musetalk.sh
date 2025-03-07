echo "Checking if 'results' folder exists..."
if [ ! -d "results" ]; then
    echo "Creating 'results' folder..."
    mkdir results
else
    echo "'results' folder already exists."
fi

git clone https://github.com/TMElyralab/MuseTalk.git

SRC_FILE="download_musetalk_model_weights.py"
DEST_DIR="MuseTalk"

if [ -f "$SRC_FILE" ]; then
    mv "$SRC_FILE" "$DEST_DIR/"
    echo "Moved $SRC_FILE to $DEST_DIR"
fi

SRC_FILE="down_ffmpeg.py"

if [ -f "$SRC_FILE" ]; then
    mv "$SRC_FILE" "$DEST_DIR/"
    echo "Moved $SRC_FILE to $DEST_DIR"
fi

SRC_FILE="create_yaml.py"

if [ -f "$SRC_FILE" ]; then
    mv "$SRC_FILE" "$DEST_DIR/"
    echo "Moved $SRC_FILE to $DEST_DIR"
fi

SRC_FILE="results/output_resynthesized.wav"
DEST_DIR="MuseTalk/data/audio"

if [ -f "$SRC_FILE" ]; then
    cp "$SRC_FILE" "$DEST_DIR/"
    echo "Copied $SRC_FILE to $DEST_DIR"
fi


video_file="$1"
if [ -z "$video_file" ]; then
    echo "Error: Please provide the path to the video file as an argument."
    exit 1
fi

SRC_FILE="$video_file"
DEST_DIR="MuseTalk/data/video"

if [ -f "$SRC_FILE" ]; then
    cp "$SRC_FILE" "$DEST_DIR/"
    echo "Copied $SRC_FILE to $DEST_DIR"
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

pip uninstall huggingface_hub --yes
pip install huggingface_hub==0.25.0

python download_musetalk_model_weights.py
python down_ffmpeg.py

export FFMPEG_PATH=/musetalk/ffmpeg-4.4-amd64-static

python create_yaml.py "$video_file"

cd ..

deactivate
