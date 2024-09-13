import torch.nn.functional as F
import torch.nn as nn
import torch


#growth rate, defined in the paper as 10
k = 10

class WideLayer(nn.Module):
    def __init__(self, in_channels, out_channels, train = True, stride = 1):
        super(WideLayer, self).__init__()

        self.conv1 = nn.Sequential(
            nn.BatchNorm2d(in_channels),
            nn.ReLU(),
            nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1)
        )
        self.conv2 = nn.Sequential(
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
            nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=stride, padding=1)
        )

        self.trans_conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=1, stride=stride)

        self.drop1 = nn.Dropout(0.35)

        self.train = train


    def forward(self, x):
        _x = x

        x = self.conv1(x)
        x = self.drop1(x) if self.train else x
        x = self.conv2(x)

        if _x.shape != x.shape: # transition layer
            _x = self.trans_conv(_x)

        x = torch.add(_x, x)

        return x


class WideBlock(nn.Module):
    def __init__(self, N, in_channels, out_channels, stride = 1):
        super(WideBlock, self).__init__()

        self.layer_num = N
        self.block_layers = nn.ModuleList()

        self.block_layers.add_module(f'WideLayer_0', WideLayer(in_channels, out_channels, stride=stride))

        for i in range(self.layer_num-1):
            self.block_layers.add_module(f'WideLayer_{i+1}', WideLayer(out_channels, out_channels))


    def forward(self, x):
        for layer in self.block_layers:
            x = layer(x)

        return x

    def set_train(self, train):
        for layer in self.block_layers:
            layer.train = train


class WideResNet(nn.Module):
    def __init__(self, depth, k, in_channels, num_classes):
        super(WideResNet, self).__init__()

        self.conv1 = nn.Sequential(
            nn.BatchNorm2d(in_channels),
            nn.ReLU(),
            nn.Conv2d(in_channels=in_channels, out_channels=16, kernel_size=3, stride=2, padding=0)
        )
        # out size: 50x50 or 42x42

        N = int((depth-4)/6)

        self.conv2 = WideBlock(N, 16, out_channels=16*k, stride=2)
        # out size: 25x25 or 21x21

        self.conv3 = WideBlock(N, 16*k, out_channels=32*k, stride=2)
        # out size: 12x12 or 10x10

        self.conv4 = WideBlock(N, 32*k, out_channels=64*k, stride=2)
        # out size: 6x6 or 5x5

        self.avg_pool = nn.Sequential(
            nn.BatchNorm2d(64*k),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1)
        )

        self.out = nn.Linear(64*k, num_classes)


    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)

        x = self.avg_pool(x)

        x = torch.flatten(x, start_dim=1)

        x = self.out(x)

        return x


    def set_train(self, train):
        self.conv2.set_train(train)
        self.conv3.set_train(train)
        self.conv4.set_train(train)
