import os
import requests
import tarfile

FFMPEG_URL = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
DEST_DIR = "./musetalk"
FFMPEG_PATH = os.path.join(DEST_DIR, "ffmpeg-4.4-amd64-static")


def download_ffmpeg(url, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    archive_path = os.path.join(dest_dir, "ffmpeg-static.tar.xz")

    print("Downloading ffmpeg-static...")
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    with open(archive_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print("Extracting ffmpeg-static...")
    with tarfile.open(archive_path, "r:xz") as tar:
        tar.extractall(dest_dir)

    os.remove(archive_path)


def set_ffmpeg_path(path):
    os.environ["FFMPEG_PATH"] = path
    print(f"FFMPEG_PATH set to {path}")


if __name__ == "__main__":
    try:
        download_ffmpeg(FFMPEG_URL, DEST_DIR)
        set_ffmpeg_path(FFMPEG_PATH)
    except Exception as e:
        print(f"Error: {e}")

