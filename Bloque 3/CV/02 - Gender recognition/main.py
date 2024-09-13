from torch.utils.data import TensorDataset, DataLoader, WeightedRandomSampler
import torchvision.transforms as transforms
from networks.WideResNet import WideResNet
from networks.DenseNet import DenseNet
from torchvision.transforms import v2
from networks.mininet import Mininet
from LFW_dataset import LFWDataset
from networks.VGG16 import VGG16
from torchsummary import summary
import torch.optim as optim
import torch.nn as nn
import numpy as np
import torchvision
import torch
import sys
import os 

path = os.getcwd()


# Data Loading Section

x_train = np.load(f'{path}/data/x_train.npy')
x_test = np.load(f'{path}/data/x_test.npy')

y_train = np.load(f'{path}/data/y_train.npy')
y_test = np.load(f'{path}/data/y_test.npy')

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

y_train = y_train.astype('float32')
y_test = y_test.astype('float32')

print(x_train.shape)
print(x_test.shape)

class_counts = [len(y_train)-sum(y_train), sum(y_train)]
sample_weights = [1/class_counts[int(i)] for i in y_train]
assert len(sample_weights) == len(y_train) 

proportion = (len(y_train)-sum(y_train))/sum(y_train)

mean = np.mean(x_train, axis=(0,1,2)) # computes mean across all channels
std = np.std(x_train, axis=(0,1,2))

norm_transforms = [
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
]

if len(sys.argv) > 1:
    args = sys.argv[1:]
    print(args)
    trans = str(args[0])                                # 0: horizontal flip; 1: random rotation; 2: random shift; 3: random crop; 
    b_size = int(args[1])                               # batch size, default 4096
    n_ep = int(args[2])                                 # num epochs, default 300
    weighten_type = int(args[3])                        # 0: none, 1: loss, 2: batch 
    net_tp = int(args[4])                               # 0: VGG; 1: DenseNet; 2: WideresNet, 3: mininet
    net_width = str(args[5]) if len(args)>5 else ''     # Only for DenseNet. 'S', 'M', 'L', 'XL'
    img_size = int(args[6]) if len(args)>6 else 100

# Data Augmentation Section

transformations = []

if trans.__contains__('3'): # center crop -> removes first and last 20 pixels
    transformations.append(v2.CenterCrop((img_size, img_size)))

if trans.__contains__('0'): # horizontal flip
    transformations.append(v2.RandomHorizontalFlip(0.5))

if trans.__contains__('1'): # rotation
    transformations.append(v2.RandomRotation(degrees=(-15, 15)))

if trans.__contains__('2'): # shift
    transformations.append(v2.RandomAffine(degrees=0, translate=(0.1, 0.1)))

transform = transforms.Compose(transformations)
norm_transform = transforms.Compose(norm_transforms)

batch_size = b_size if b_size else 4096
epochs = n_ep if n_ep else 300

train_set = LFWDataset(x_train, y_train, norm_transform=norm_transform, transform=transform)
# train_set, dev_set = torch.utils.data.random_split(train_set, [0.8, 0.2])
test_set = LFWDataset(x_test, y_test, norm_transform=norm_transform, transform=transform if net_tp == 3 else None)

if weighten_type == 0 or weighten_type == 1:
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=1)
if weighten_type == 2:
    weighted_train_sampler = WeightedRandomSampler(weights=sample_weights, num_samples=len(y_train), replacement=True)
    train_loader = DataLoader(train_set, sampler=weighted_train_sampler, batch_size=batch_size)

dev_loader = DataLoader(test_set, batch_size=batch_size, shuffle=True, num_workers=1)
test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=True, num_workers=1)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Model Creation Section

if net_tp == 0:
    model_str = 'vggB'
    net = VGG16()
if net_tp == 1:
    model_str = 'DenseNet' + net_width
    size = [6,12,24,16]
    # size = [6, 12, 18, 12]
    if net_width == 'M':
        size = [6,12,32,32]
    if net_width == 'L':
        size = [6,12,48,32]
    if net_width == 'XL':
        size = [6,12,64,48]
    net = DenseNet(size, num_classes = 2)
if net_tp == 2:
    model_str = 'WideResNet'
    net = WideResNet(depth=28, k=10, in_channels = 3, num_classes = 2)
    
if net_tp == 3:
    net = Mininet()
    model_str = 'mininet'

if trans.__contains__('0'):
    model_str += '_hf'
if trans.__contains__('2'):
    model_str += '_shift'
if trans.__contains__('3'):
    model_str += '_crop'
if trans.__contains__('1'):
    model_str += '_rot'

if weighten_type == 0:
    model_str += '_imbalanced'
if weighten_type == 1:
    model_str += '_weightedLoss'
if weighten_type == 2:
    model_str += '_weightedBatch'

if net_tp == 3:
    model_str += f'_{img_size}'

# Optimizer Section
    
net.to(device)
    
if net_tp == 3:
    summary(net, input_size=(3, img_size, img_size))


if weighten_type == 1: 
    loss_fn = nn.CrossEntropyLoss(weight=torch.tensor([1, proportion], device=device, dtype=torch.float32))
else:
    loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.0001, weight_decay=1e-3)
# optimizer = optim.SGD(net.parameters(),lr=0.1, weight_decay=1e-4)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, min_lr=0.00001, patience=10)


# Training Loop Section

import time
min_loss = 100000
early_stp = 0
for epoch in range(epochs):

    running_loss = 0.0
    start = time.time()
    for i, data in enumerate(train_loader, 0):

        inputs, labels = data[0].to(device), data[1].to(device)
        # zero the parameter gradients
        optimizer.zero_grad()

        outputs = net(inputs)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    total_dev_loss = 0
    net.set_train(False)
    with torch.no_grad():
        for data in dev_loader:
            inputs, labels = data[0].to(device), data[1].to(device)

            outputs = net(inputs)
            val_loss = loss_fn(outputs, labels)
            total_dev_loss += val_loss

        if total_dev_loss < min_loss:
            early_stp = 0
            min_loss = total_dev_loss
            torch.save(net.state_dict(), f'{os.getcwd()}/models/{model_str}_drop.pt')
        else:
            early_stp+= 1
    scheduler.step(total_dev_loss)
    net.set_train(True)
    end = time.time()

    if early_stp == 35:
        break

    # print statistics
    print(f'epoch: {epoch + 1} ({end-start:.2f}s) -- loss: {running_loss / len(train_loader):.4f} -- dev_loss: {total_dev_loss / len(dev_loader):.4f} -- ETA: {(end-start) * (epochs-epoch):.2f}s\n')


# Test Loop Section
correct = 0
total = 0
net.load_state_dict(torch.load(f'{os.getcwd()}/models/{model_str}_drop.pt'))
with torch.no_grad():
    net.set_train(False)
    for data in test_loader:
        inputs, labels = data[0].to(device), data[1].to(device)

        outputs = net(inputs)

        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
net.set_train(True)
print(f'Accuracy of the network {model_str} on the {total} test images: {(100 * correct / total):.02f} %')
