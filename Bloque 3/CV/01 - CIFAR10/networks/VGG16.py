import torch.nn.functional as F
import torch.nn as nn
import torch


class VGG16(nn.Module):
    def __init__(self, train=True):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Conv2d(512, 512, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Conv2d(512, 512, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
        )
        self.conv5 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Conv2d(512, 512, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Conv2d(512, 512, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
        )

        self.max_pool = nn.MaxPool2d(kernel_size=(2,2), stride=2)

        self.drop1 = nn.Dropout(0.25)
        self.drop2 = nn.Dropout(0.25)
        self.drop3 = nn.Dropout(0.25)
        self.drop4 = nn.Dropout(0.25)
        self.drop5 = nn.Dropout(0.25)
        self.drop6 = nn.Dropout(0.5)
        self.drop7 = nn.Dropout(0.5)

        self.relu = nn.ReLU()

        self.h1 = nn.Linear(in_features=512, out_features=4096)
        self.h2 = nn.Linear(in_features=4096, out_features=4096)
        self.out = nn.Linear(in_features=4096, out_features=10)

        self.train = train


    def set_train(self, train):
        self.train = train


    def forward(self, x):
        # 32x32x3 -> 16x16x32
        y = self.conv1(x)
        y = self.max_pool(y)
        y = self.drop1(y) if self.train else y

        # 16x16x32 -> 8x8x64
        y = self.conv2(y)
        y = self.max_pool(y)
        y = self.drop2(y) if self.train else y

        # 8x8x64 -> 4x4x128
        y = self.conv3(y)
        y = self.max_pool(y)
        y = self.drop3(y) if self.train else y

        # 4x4x128 -> 2x2x256
        y = self.conv4(y)
        y = self.max_pool(y)
        y = self.drop4(y) if self.train else y

        # 2x2x256 -> 1x1x512
        y = self.conv5(y)
        y = self.max_pool(y)
        y = self.drop5(y) if self.train else y

        y = torch.flatten(y, 1)

        y = self.h1(y)
        y = self.relu(y)
        y = self.drop6(y) if self.train else y
        y = self.h2(y)
        y = self.relu(y)
        y = self.drop7(y) if self.train else y
        out = self.out(y)

        return out
