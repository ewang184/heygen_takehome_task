cd MuseTalk

video_file="$1"
if [ -z "$video_file" ]; then
    echo "Error: Please provide the path to the video file as an argument."
    exit 1
fi

video_name="${video_file%.mp4}"

VENV_PATH="muse_env/bin/activate"

if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    echo "Virtual environment activated."

else
    echo "Error: Virtual environment activate script not found."
    exit 1
fi

python -m scripts.inference --inference_config configs/inference/takehome.yaml 

deactivate

SRC_FILE="results/${video_name}_output_resynthesized.mp4"
DEST_DIR="./../results/"

if [ -f "$SRC_FILE" ]; then
    cp "$SRC_FILE" "$DEST_DIR/"
    echo "Moved $SRC_FILE to $DEST_DIR"
fi

cd ..
