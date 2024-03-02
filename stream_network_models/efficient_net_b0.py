"""
File: efficient_net_b0.py
Author: Richárd Rádli
E-mail: radli.richard@mik.uni-pannon.hu
Date: May 06, 2023

Description: The program implements the EfficientNet b0 with custom linear layer.
"""

import torch
import torch.nn as nn
import torchvision.models as models


class EfficientNet(nn.Module):
    def __init__(self, num_out_feature: int = 128, grayscale=True):
        """
        EfficientNet model with custom linear layer.

        :param num_out_feature: Number of output features.
        :param grayscale: Whether the input is grayscale or not. Defaults to True.
        """

        super(EfficientNet, self).__init__()
        self.num_out_feature = num_out_feature
        self.grayscale = grayscale
        self.model = self.build_model()
        if self.grayscale:
            self.model.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=2, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the EfficientNet model.

        :param x: Input tensor.
        :return: Output tensor.
        """

        if self.grayscale:
            x = x.expand(-1, 3, -1, -1)
        x = self.model(x)
        return x

    def build_model(self) -> nn.Module:
        """
        Build the EfficientNet model with a custom linear layer.

        :return: EfficientNet model with custom linear layer.
        """

        model = models.efficientnet_b0(weights='DEFAULT')
        model.classifier[1] = nn.Linear(in_features=1280, out_features=self.num_out_feature)
        return model
