import os
from pathlib import Path

import cv2
import torch
import numpy as np

from torch.utils.data import Dataset


class BrainTumorDataset(Dataset):

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.image_mask_pairs = []

        self._load_dataset()

    def __len__(self):
        return len(self.image_mask_pairs)

    def __getitem__(self, index):
        pass

    def _load_dataset(self):
    # Loop through every patient folder
        for patient_folder in self.root_dir.iterdir():

        # Skip anything that isn't a folder
           if not patient_folder.is_dir():
            continue

           print(f"Scanning: {patient_folder.name}")