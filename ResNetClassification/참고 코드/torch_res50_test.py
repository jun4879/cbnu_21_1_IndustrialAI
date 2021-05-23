import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F

if torch.cuda.is_available():
    DEVICE = torch.device('cuda')
else:
    DEVICE = torch.device('cpu')

BATCH_SIZE = 32
EPOCHS = 10

class BasicBlock(nn.Module):
    def __init__(self, input_nodes, mid_nodes, out_nodes, stride=1):
        super(BasicBlock, self).__init__()
        # padding valid : 1x1 커널이므로 패딩 없이 주어야 이미지 사이즈 그대로
        self.conv1 = nn.Conv2d(input_nodes, mid_nodes, kernel_size=1, stride=stride)
        self.bn1 = nn.BatchNorm2d(mid_nodes)
        # padding same : 3x3 커널이므로 패딩을 주어야 이미지 사이즈 그대로
        self.conv2 = nn.Conv2d(mid_nodes, mid_nodes, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(mid_nodes)
        # padding valid : 1x1 커널이므로 패딩 없이 주어야 이미지 사이즈 그대로
        self.conv3 = nn.Conv2d(mid_nodes, out_nodes, kernel_size=1, stride=stride)
        self.bn3 = nn.BatchNorm2d(out_nodes)

        self.shortcut = nn.Sequential()
        if stride != 1 or input_nodes != out_nodes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(input_nodes, out_nodes, kernel_size=1, stride=stride),
                nn.BatchNorm2d(out_nodes))

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))

        out = self.bn3(self.conv3(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class ResNet50(nn.Module):
    def __init__(self, num_classes=6):
        super(ResNet50, self).__init__()
        self.input_nodes = 64
        ## conv1_block
        # zero_padding
        self.zero_pad = nn.ZeroPad2d(1)
        # conv : input_node = 3, output_node = 64, // padding = 1?
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=1)
        # batch_normal
        self.bn = nn.BatchNorm2d(64)
        # 2block 전 maxpool
        self.max_pool = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        self.layer1 = self._make_layer(64, 64, 256, 3, stride=1)
        self.layer2 = self._make_layer(128, 128, 512, 4, stride=2)
        self.layer3 = self._make_layer(256, 256, 1024, 6, stride=2)
        self.layer4 = self._make_layer(512, 512, 2048, 3, stride=2)
        self.linear = nn.Linear(2048, num_classes) # 마지막 out_node에 맞게 2048, num_classes = 카테고리 6개

    def _make_layer(self, input_nodes, mid_nodes, out_nodes, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(BasicBlock(self.input_nodes, mid_nodes, out_nodes, stride))
        return nn.Sequential(*layers)

    def forward(self, x):
        out = self.zero_pad(F.relu(self.bn(self.conv1(self.zero_pad(x)))))
        out = self.max_pool(out)
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 2)  # 2x2 size filter
        out = out.view(out.size(0), -1)
        out = self.linear(out)
        return out

model = ResNet50().to(DEVICE)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

print(model)