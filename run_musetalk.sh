cd MuseTalk

VENV_PATH="muse_env/bin/activate"

if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    echo "Virtual environment activated."

else
    echo "Error: Virtual environment activate script not found."
    exit 1
fi

python -m scripts.inference --inference_config configs/inference/takehome.yaml 

source deactivate

cd ..

SRC_FILE="MuseTalk/results/${video_file}_output_resynthesized.mp4"
DEST_DIR="./"

if [ -f "$SRC_FILE" ]; then
    mv "$SRC_FILE" "$DEST_DIR/"
    echo "Moved $SRC_FILE to $DEST_DIR"
fi
