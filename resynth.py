import os
import json
import torch
from scipy.io.wavfile import write
from env import AttrDict
from meldataset import mel_spectrogram, MAX_WAV_VALUE, load_wav
from models import Generator
from stft import TorchSTFT
from Utils.JDC.model import JDCNet
import glob

def load_checkpoint(filepath, device):
    assert os.path.isfile(filepath)
    print(f"Loading checkpoint from '{filepath}'")
    checkpoint_dict = torch.load(filepath, map_location=device)
    print("Checkpoint loaded successfully.")
    return checkpoint_dict

def get_mel(x, h):
    return mel_spectrogram(x, h.n_fft, h.num_mels, h.sampling_rate, h.hop_size, h.win_size, h.fmin, h.fmax)

def scan_checkpoint(cp_dir, prefix):
    cp_list = sorted(glob.glob(os.path.join(cp_dir, prefix + '*')))
    return cp_list[-1] if cp_list else ''

def resynthesize_audio(input_wav_path, output_wav_path, cp_path="cp_hifigan"):
    # Load HiFTNet configuration
    with open(os.path.join(cp_path, "config.json")) as f:
        json_config = json.load(f)
    h = AttrDict(json_config)

    # Set device
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    # Load models
    F0_model = JDCNet(num_class=1, seq_len=192)
    generator = Generator(h, F0_model).to(device)
    stft = TorchSTFT(filter_length=h.gen_istft_n_fft, hop_length=h.gen_istft_hop_size, win_length=h.gen_istft_n_fft).to(device)

    # Load generator checkpoint
    cp_g = scan_checkpoint(cp_path, 'g_')
    state_dict_g = load_checkpoint(cp_g, device)
    generator.load_state_dict(state_dict_g['generator'])
    generator.remove_weight_norm()
    generator.eval()

    # Load and normalize input audio
    wav, sr = load_wav(input_wav_path)
    wav = wav / MAX_WAV_VALUE
    wav = torch.FloatTensor(wav).to(device)

    # Compute mel spectrogram
    mel = get_mel(wav.unsqueeze(0), h)

    # Resynthesize audio
    with torch.no_grad():
        spec, phase = generator(mel)
        y_g_hat = stft.inverse(spec, phase)
        audio = y_g_hat.squeeze() * MAX_WAV_VALUE
        audio = audio.cpu().numpy().astype('int16')

    # Save the resynthesized audio
    write(output_wav_path, sr, audio)

resynthesize_audio("./../warped_german_voice.wav", "./../results/output_resynthesized.wav")
