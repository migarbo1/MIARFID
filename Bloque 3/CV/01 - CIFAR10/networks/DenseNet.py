import torch.nn.functional as F
import torch.nn as nn
import torch


#growth rate, defined in the paper as 12
k = 12

class DenseLayer(nn.Module):
    def __init__(self, in_channels, train = True):
        super(DenseLayer, self).__init__()

        self.conv1 = nn.Sequential(
            nn.BatchNorm2d(in_channels),
            nn.ReLU(),
            nn.Conv2d(in_channels=in_channels, out_channels=4*k, kernel_size=1, stride=1, padding=0, bias = False)
        )
        self.conv2 = nn.Sequential(
            nn.BatchNorm2d(4*k),
            nn.ReLU(),
            nn.Conv2d(in_channels=4*k, out_channels=k, kernel_size=3, stride=1, padding=1, bias = False)
        )

        self.drop1 = nn.Dropout(0.2)

        self.train = train

        
    def forward(self, x):
        _x = x

        x = self.conv1(x)
        x = self.conv2(x)
        x = self.drop1(x) if self.train else x

        x = torch.cat([_x, x], 1)

        return x
    

class DenseBlock(nn.Module):
    def __init__(self, layer_num, in_channels):
        super(DenseBlock, self).__init__()

        self.layer_num = layer_num
        self.block_layers = nn.ModuleList()

        for i in range(self.layer_num):
            self.block_layers.add_module(f'DenseLayer_{i}', DenseLayer(in_channels + k*i))


    def forward(self, x):
        for layer in self.block_layers:
            x = layer(x)

        return x
   
    def set_train(self, train):
        for layer in self.block_layers:
            layer.train = train


class TransitionLayer(nn.Module):
    def __init__(self, in_channels, compression_factor = 0.5):
        super(TransitionLayer, self).__init__()

        self.conv_block = nn.Sequential(
                nn.BatchNorm2d(in_channels),
                nn.Conv2d(in_channels=in_channels, out_channels=int(in_channels*compression_factor), kernel_size=1, stride=1, padding=0, bias=False),
                nn.AvgPool2d(kernel_size=2, stride=2) 
            )
    
    
    def forward(self, x):

        x = self.conv_block(x)

        return x
    

class DenseNet(nn.Module):
    def __init__(self, shape, in_channels = 3, num_classes = 10, compression_factor = 0.5, train = True):
        super(DenseNet, self).__init__()

        self.train = train

        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=64, kernel_size=3, stride=1, padding=1, bias=True),
            nn.BatchNorm2d(64),
            nn.ReLU()
        )

        self.blocks = nn.ModuleList()
        dense_block_inchannels = 64

        for i in range(len(shape)-1):
            self.blocks.add_module(f'DenseBlock_{i}', DenseBlock(shape[i], dense_block_inchannels))
            dense_block_inchannels = int(dense_block_inchannels + k*shape[i])

            self.blocks.add_module(f'TransitionLayer_{i}', TransitionLayer(dense_block_inchannels, compression_factor))
            dense_block_inchannels = int(dense_block_inchannels*compression_factor)

        self.blocks.add_module(f'DenseBlock_{i+1}', DenseBlock(shape[-1], dense_block_inchannels))
        dense_block_inchannels = int(dense_block_inchannels + k*shape[-1])

        self.glob_avg_pool_layer = nn.Sequential(
            nn.BatchNorm2d(dense_block_inchannels),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1)
        )

        self.out = nn.Linear(dense_block_inchannels, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        
        for layer in self.blocks:
            x = layer(x)

        x = self.glob_avg_pool_layer(x)

        x = torch.flatten(x, start_dim=1)
        x = self.out(x)

        return x

    def set_train(self, train):
        self.train = train
        for name, layer in self.named_modules():
            if name.startswith('DenseBlock'):
                layer.set_train(train)
