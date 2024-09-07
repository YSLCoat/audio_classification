import os
import pandas as pd
import torch
from torch.utils.data import Dataset
import torchaudio

torchaudio.set_audio_backend("soundfile")


class UrbanSoundDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        Args:
            root_dir (str): Directory with all the audio subfolders.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.root_dir = root_dir
        self.metadata_path = os.path.join(self.root_dir, r"metadata\UrbanSound8K.csv")
        self.metadata = pd.read_csv(self.metadata_path)
        self.transform = transform

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        audio_info = self.metadata.iloc[idx]
        fold = f"fold{audio_info['fold']}"
        file_name = audio_info['slice_file_name']
        file_path = os.path.join(self.root_dir, "audio", fold, file_name)

        waveform, sample_rate = torchaudio.load(file_path)

        label = audio_info['classID']
        class_name = audio_info['class']

        sample = {'waveform': waveform, 'sample_rate': sample_rate, 'label': label, 'class': class_name}

        if self.transform:
            sample = self.transform(sample)

        return sample