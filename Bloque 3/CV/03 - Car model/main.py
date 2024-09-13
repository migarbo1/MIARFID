from torch.utils.data import TensorDataset, DataLoader, WeightedRandomSampler
from networks.BilinearVGG import BilinearNet
import torchvision.transforms as transforms
from torchvision.transforms import v2
from Car_dataset import CarDataset
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

y_train = y_train - 1
y_test = y_test - 1

print(x_train.shape)
print(x_test.shape)

mean = np.mean(x_train, axis=(0,1,2)) # computes mean across all channels
std = np.std(x_train, axis=(0,1,2))

if len(sys.argv) > 1:
    args = sys.argv[1:]
    print(args)
    layer_num = int(args[0])                                # 0: horizontal flip; 1: random rotation; 2: random shift; 3: random crop; 
    drop = float(args[1])
    b_size = int(args[2])                               # batch size, default 4096
    n_ep = int(args[3])                                 # num epochs, default 300
    unf_ep = int(args[4])
    st_lr = str(args[5])
    min_lr = str(args[6])
    net = str(args[7])

# Data Augmentation Section

batch_size = b_size if b_size else 128
epochs = n_ep if n_ep else 50

train_set = CarDataset(x_train, y_train, net=net)
test_set = CarDataset(x_test, y_test, net=net)

train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=1)
test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=True, num_workers=1)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Model Creation Section
model_str = f'{net}_{batch_size}_{layer_num}_{int(drop*10)}_{epochs}_{unf_ep}_{st_lr}_{min_lr}'
net = BilinearNet(20, layer_num=layer_num, drop=drop, net = net)

# Optimizer Section
    
net.to(device)

if net != 'den':
    print(net)

def lr_lambda(epoch):
    if epoch == unf_ep:
        return float(min_lr)
    else:
        return float(st_lr)

loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=1e-3, weight_decay=1e-3)
# scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, min_lr=0.00001, patience=10)
scheduler = optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
# Training Loop Section

import time
best_acc = 0
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

    

    correct = 0
    total = 0
    with torch.no_grad():
        for data in test_loader:
            inputs, labels = data[0].to(device), data[1].to(device)

            outputs = net(inputs)

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    curr_acc = correct / total
    if curr_acc > best_acc:
        best_acc = curr_acc
        torch.save(net.state_dict(), f'{os.getcwd()}/models/{model_str}_drop.pt')

    scheduler.step()
    end = time.time()
    if epoch == unf_ep:
        net.set_req_grad(True)
        print('unfrozen network')
    
    print(f'epoch: {epoch+1} ({end-start:.2f}) -- loss: {running_loss / len(train_loader):.4f} -- test_accuracy: {(100*correct/total):.4f} -- ETA: {(end-start)*(epochs-epoch):.2f}\n')

# Test Loop Section
correct = 0
total = 0
net.load_state_dict(torch.load(f'{os.getcwd()}/models/{model_str}_drop.pt'))
with torch.no_grad():
    for data in test_loader:
        inputs, labels = data[0].to(device), data[1].to(device)

        outputs = net(inputs)

        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print(f'Accuracy of the network {model_str} on the {total} test images: {(100 * correct / total):.02f} %')
