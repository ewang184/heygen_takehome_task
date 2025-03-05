import os
import requests
from pathlib import Path

# Directory structure
model_paths = {
    'musetalk': [
        ('https://huggingface.co/TMElyralab/MuseTalk/blob/main/musetalk/musetalk.json', 'musetalk.json'),
        ('https://huggingface.co/TMElyralab/MuseTalk/blob/main/musetalk/pytorch_model.bin', 'pytorch_model.bin')
    ],
    'sd-vae-ft-mse': [
        ('https://huggingface.co/stabilityai/sd-vae-ft-mse/blob/main/config.json', 'config.json'),
        ('https://huggingface.co/stabilityai/sd-vae-ft-mse/blob/main/diffusion_pytorch_model.bin', 'diffusion_pytorch_model.bin')
    ],
    'whisper': [
        ('https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt', 'tiny.pt')
    ],
    'dwpose': [
        ('https://huggingface.co/yzd-v/DWPose/blob/main/dw-ll_ucoco_384.pth', 'dw-ll_ucoco_384.pth')
    ],
    'face-parse-bisent': [
        ('https://drive.google.com/uc?id=154JgKpzCPW82qINcVieuPH3fZ2e0P812', '79999_iter.pth'),
        ('https://download.pytorch.org/models/resnet18-5c106cde.pth', 'resnet18-5c106cde.pth')
    ]
}

base_dir = Path('./models')


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Downloaded: {save_path}")


def main():
    for folder, files in model_paths.items():
        folder_path = base_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)

        for url, filename in files:
            save_path = folder_path / filename
            if not save_path.exists():
                try:
                    download_file(url, save_path)
                except Exception as e:
                    print(f"Failed to download {url}: {e}")
            else:
                print(f"Already exists: {save_path}")


if __name__ == '__main__':
    main()

