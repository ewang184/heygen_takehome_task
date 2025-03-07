import yaml
from pathlib import Path
import argparse
# Script to create MuseTalk config file

parser = argparse.ArgumentParser(description="Get video name")

parser.add_argument("video_name", type=str, help="Video name")
args = parser.parse_args()

data = {
    'task_0': {
        'video_path': f'data/video/{args.video_name}',
        'audio_path': 'data/audio/output_resynthesized.wav',
        'bbox_shift': -15
    }
}

output_dir = Path('configs/inference')
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / 'takehome.yaml'

with open(output_file, 'w') as file:
    yaml.dump(data, file, default_flow_style=False)

print(f"YAML file created at: {output_file}")
