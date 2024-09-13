from torch.utils.data import Dataset
from PIL import Image
import numpy as np
import torch

class LFWDataset(Dataset):
    def __init__(self, data, targets, norm_transform, transform=None):
        self.data = data
        self.targets = torch.LongTensor(targets)
        self.norm_transform = norm_transform
        self.transform = transform


    def __getitem__(self, index):
        x = self.data[index]
        y = self.targets[index]

        x = Image.fromarray(self.data[index].astype(np.uint8))
        x = self.norm_transform(x)
        
        if self.transform:
            x = self.transform(x)

        return x, y


    def __len__(self):
        return len(self.data)
