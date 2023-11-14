import os
import torch
# path_label = ['']
# labels = []
# for i in path_label:
#     file = os.listdir(i)

import torch.nn as nn

# 定义一个二维最大池化层
maxpool_layer = nn.MaxPool2d(kernel_size=10, stride=2)

# 定义一个输入张量
input_tensor = torch.randn(1, 3, 224, 225)

# 将输入张量传递给最大池化层
output_tensor = maxpool_layer(input_tensor)

# 输出张量的形状
print(output_tensor.shape)
