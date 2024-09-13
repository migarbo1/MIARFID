from torch.utils.data import Dataset
from PIL import Image
import torchvision
import numpy as np
import torch

class CarDataset(Dataset):
    def __init__(self, data, targets, net):
        self.data = data
        self.targets = torch.LongTensor(targets)
        if net == 'vgg':
            self.transform = torchvision.models.VGG16_BN_Weights.IMAGENET1K_V1.transforms()
        if net == 'res':
            self.transform = torchvision.models.ResNet50_Weights.IMAGENET1K_V2.transforms()
        if net == 'den':
            self.transform = torchvision.models.DenseNet121_Weights.IMAGENET1K_V1.transforms()

    def __getitem__(self, index):
        x = self.data[index]
        y = self.targets[index]

        x = Image.fromarray(self.data[index].astype(np.uint8))
        
        if self.transform:
            x = self.transform(x)

        return x, y


    def __len__(self):
        return len(self.data)
