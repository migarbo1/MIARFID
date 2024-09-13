import torchvision.transforms as transforms
from networks.WideResNet import WideResNet
from networks.DenseNet import DenseNet
from torchvision.transforms import v2
from networks.VGG16 import VGG16
import torch.optim as optim
import torch.nn as nn
import numpy as np
import torchvision
import torch
import sys
import os

b_size = 4096

if len(sys.argv) > 1:
    args = sys.argv[1:]
    trans = str(args[0])                            # 0: horizontal flip; 1: random rotation; 2: gaussian blur -> '012' means all filters applied
    b_size = int(args[1])
    net_tp = int(args[2])                              # 0: VGG; 1: DenseNet
    net_width = str(args[3]) if len(args)>3 else '' # Only for DenseNet. 'S', 'M', 'L', 'XL'

# Data loading
transformations = [
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616)),
    ]

if trans.__contains__('4'):
    transformations.append(v2.Resize((36,36)))
    transformations.append(v2.RandomCrop((32,32)))

if trans.__contains__('0'):
    transformations.append(v2.RandomHorizontalFlip(0.5))

if trans.__contains__('1'):
    transformations.append(v2.RandomRotation(degrees=(-15, 15)))

if trans.__contains__('3'):
    transformations.append(v2.RandomAffine(degrees=0, translate=(0.2, 0.2)))

if trans.__contains__('2'):
    transformations.append(v2.GaussianBlur(kernel_size=(3,3)))

transform = transforms.Compose(transformations)

batch_size = b_size

print('batch_size:', b_size)

trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=1)

testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform= transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616)),
]))

_, devset = torch.utils.data.random_split(testset, [0.7, 0.3])

testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=1)
devloader = torch.utils.data.DataLoader(devset, batch_size=batch_size, shuffle=False, num_workers=1)

classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# Net and optimizer creation
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

net = None

print(net_tp)

if net_tp == 0:
    net = VGG16()

if net_tp == 1:
    print('DenseNet')
    size = [6,12,24]
    if net_width == 'M':
        size = [6,12,32]
    if net_width == 'L':
        size = [6,12,48]
    if net_width == 'XL':
        size = [6,12,64]
    net = DenseNet(size)

if net_tp == 2:
    net = WideResNet(depth=28, k=10, in_channels = 3, num_classes = 10)

net.to(device)
loss_fn = nn.CrossEntropyLoss()
# optimizer = optim.Adam(net.parameters(), lr=0.001, weight_decay=1e-4)
optimizer = optim.SGD(net.parameters(),lr=0.1, weight_decay=1e-4)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, min_lr=0.00001, patience=10)

# model name set based on input parameters
model_str = 'vggB' if net_tp == 0 else ''
model_str = 'DenseNet' if net_tp == 1 else model_str
model_str = 'WideResNet' if net_tp == 2 else model_str

model_str = model_str + net_width if net_tp == 1 else model_str

if trans.__contains__('0'):
    model_str += '_hf'

if trans.__contains__('2'):
    model_str += '_gb'

if trans.__contains__('3'):
    model_str += '_shift'

if trans.__contains__('1'):
    model_str += '_rot'

if trans.__contains__('4'):
    model_str += '_crop'

# Training loop
import time
min_loss = 100000
epochs = 300
early_stp = 0
for epoch in range(epochs):

    running_loss = 0.0
    start = time.time()
    for i, data in enumerate(trainloader, 0):

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
        for data in devloader:
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
    print(f'epoch: {epoch + 1} ({end-start:.2f}s) -- loss: {running_loss / len(trainloader):.4f} -- dev_loss: {total_dev_loss / len(devloader):.4f} -- ETA: {(end-start) * (epochs-epoch):.2f}s\n')

# Test loop: expected accuracy around 0.88
correct = 0
total = 0
net.load_state_dict(torch.load(f'{os.getcwd()}/models/{model_str}_drop.pt'))
with torch.no_grad():
    net.set_train(False)
    for data in testloader:
        inputs, labels = data[0].to(device), data[1].to(device)

        outputs = net(inputs)

        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
net.set_train(True)
print(f'Accuracy of the network {model_str} on the {total} test images: {(100 * correct / total):.02f} %')
