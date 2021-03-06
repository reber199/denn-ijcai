# CODE ADAPTED FROM https://github.com/hendrycks/outlier-exposure
import torch
import torch.nn as nn
import torch.nn.functional as F


def gelu(x):
    return torch.sigmoid(1.702 * x) * x
    # return 0.5 * x * (1 + torch.tanh(x * 0.7978845608 * (1 + 0.044715 * x * x)))


class ConvNet(nn.Module):

    def __init__(self):
        super(ConvNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = gelu(F.max_pool2d(self.conv1(x), 2))
        x = gelu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = gelu(self.fc1(x))
        # x = F.dropout(x)
        return self.fc2(x)


class NNMNIST(nn.Module):

    def __init__(self, input_size, output_size, n_neurons=200):
        super().__init__()

        # Architecture construction
        self.fc1 = nn.Linear(input_size, n_neurons)
        self.fc1_bn = nn.BatchNorm1d(n_neurons)
        self.fc2 = nn.Linear(n_neurons, n_neurons)
        self.fc2_bn = nn.BatchNorm1d(n_neurons)
        self.fc3 = nn.Linear(n_neurons, n_neurons)
        self.fc3_bn = nn.BatchNorm1d(n_neurons)
        self.fco = nn.Linear(n_neurons, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc1_bn(x)
        x = F.relu(self.fc2(x))
        x = self.fc2_bn(x)
        x = F.relu(self.fc3(x))
        x = self.fc3_bn(x)
        return self.fco(x)
