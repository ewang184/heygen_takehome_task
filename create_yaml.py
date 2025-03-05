import yaml
from pathlib import Path

# Script to create MuseTalk config file

data = {
    'task_0': {
        'video_path': 'data/video/Tanzania-2.mp4',
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
