"""
File: efficient_net_v2_s_multihead_attention.py
Author: Richárd Rádli
E-mail: radli.richard@mik.uni-pannon.hu
Date: Jul 19, 2023

Description: The program implements the EfficientNetV2 small with multiple multi-head attention with Fusion Net.
"""

import torch
import torch.nn as nn

from config.config import ConfigStreamNetwork
from stream_network_models.stream_network_selector import NetworkFactory
from utils.utils import find_latest_file_in_latest_directory


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++ E F F I C I E N T N E T V 2 M U L T I H E A D A T T E N T I O N +++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EfficientNetV2MHAFMHA(nn.Module):
    def __init__(self, type_of_net, network_cfg_contour, network_cfg_lbp, network_cfg_rgb, network_cfg_texture) -> None:
        """
        This is the initialization function of the EfficientNetV2MHAFMHA class.

        :param type_of_net: Type of network to create.
        :param network_cfg_contour: Configuration for the contour network.
        :param network_cfg_lbp: Configuration for the LBP network.
        :param network_cfg_rgb: Configuration for the RGB network.
        :param network_cfg_texture: Configuration for the texture network.
        """

        super(EfficientNetV2MHAFMHA, self).__init__()

        stream_net_cfg = ConfigStreamNetwork().parse()

        latest_con_pt_file = find_latest_file_in_latest_directory(
            path=(
                network_cfg_contour
                .get("model_weights_dir")
                .get("EfficientNetV2")
                .get(stream_net_cfg.dataset_type)
            ),
            type_of_loss=stream_net_cfg.type_of_loss_func
        )
        latest_lbp_pt_file = find_latest_file_in_latest_directory(
            path=(
                network_cfg_lbp
                .get("model_weights_dir")
                .get("EfficientNetV2")
                .get(stream_net_cfg.dataset_type)
            ),
            type_of_loss=stream_net_cfg.type_of_loss_func
        )
        latest_rgb_pt_file = find_latest_file_in_latest_directory(
            path=(
                network_cfg_rgb
                .get("model_weights_dir")
                .get("EfficientNetV2")
                .get(stream_net_cfg.dataset_type)
            ),
            type_of_loss=stream_net_cfg.type_of_loss_func
        )
        latest_tex_pt_file = find_latest_file_in_latest_directory(
            path=(
                network_cfg_texture
                .get("model_weights_dir")
                .get("EfficientNetV2")
                .get(stream_net_cfg.dataset_type)
            ),
            type_of_loss=stream_net_cfg.type_of_loss_func
        )

        self.contour_network = NetworkFactory.create_network(type_of_net, network_cfg_contour)
        self.lbp_network = NetworkFactory.create_network(type_of_net, network_cfg_lbp)
        self.rgb_network = NetworkFactory.create_network(type_of_net, network_cfg_rgb)
        self.texture_network = NetworkFactory.create_network(type_of_net, network_cfg_texture)

        self.contour_network.load_state_dict(torch.load(latest_con_pt_file))
        self.lbp_network.load_state_dict(torch.load(latest_lbp_pt_file))
        self.rgb_network.load_state_dict(torch.load(latest_rgb_pt_file))
        self.texture_network.load_state_dict(torch.load(latest_tex_pt_file))

        self.multi_head_con = nn.MultiheadAttention(embed_dim=network_cfg_contour.get("embedded_dim"), num_heads=4)
        self.multi_head_lbp = nn.MultiheadAttention(embed_dim=network_cfg_lbp.get("embedded_dim"), num_heads=4)
        self.multi_head_rgb = nn.MultiheadAttention(embed_dim=network_cfg_rgb.get("embedded_dim"), num_heads=4)
        self.multi_head_tex = nn.MultiheadAttention(embed_dim=network_cfg_texture.get("embedded_dim"), num_heads=4)

        input_dim = (network_cfg_contour.get("embedded_dim") +
                     network_cfg_lbp.get("embedded_dim") +
                     network_cfg_rgb.get("embedded_dim") +
                     network_cfg_texture.get("embedded_dim"))

        self.multi_head = nn.MultiheadAttention(embed_dim=input_dim, num_heads=4)

        self.multi_head_modules = {
            "contour": self.multi_head_con,
            "lbp": self.multi_head_lbp,
            "rgb": self.multi_head_rgb,
            "texture": self.multi_head_tex,
            "fusion": self.multi_head
        }

        self.fc1 = nn.Linear(input_dim, input_dim)
        self.fc2 = nn.Linear(input_dim, input_dim)
        self.relu = nn.ReLU()

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------- F O R W A R D --------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def forward(self, contour_tensor: torch.Tensor, lbp_tensor: torch.Tensor, rgb_tensor: torch.Tensor,
                texture_tensor: torch.Tensor):
        """
        This is the forward function of the FusionNet.

        Args:
            contour_tensor: input tensor for contour stream, with shape [batch_size, 1, height, width]
            lbp_tensor: input tensor for LBP stream, with shape [batch_size, 1, height, width]
            rgb_tensor: input tensor for RGB stream, with shape [batch_size, 3, height, width]
            texture_tensor: input tensor for texture stream, with shape [batch_size, 1, height, width]

        Returns:
             output tensor with shape [batch_size, 640] after passing through fully connected layers.
        """

        contour_tensor = self.contour_network(contour_tensor)
        lbp_tensor = self.lbp_network(lbp_tensor)
        rgb_tensor = self.rgb_network(rgb_tensor)
        texture_tensor = self.texture_network(texture_tensor)

        contour_tensor = self.multi_head_attention(contour_tensor, sub_stream="contour")
        lbp_tensor = self.multi_head_attention(lbp_tensor, sub_stream="lbp")
        rgb_tensor = self.multi_head_attention(rgb_tensor, sub_stream="rgb")
        texture_tensor = self.multi_head_attention(texture_tensor, sub_stream="texture")

        concatenated = torch.cat(
            (contour_tensor, lbp_tensor, rgb_tensor, texture_tensor), dim=1
        )
        concatenated = self.multi_head_attention(concatenated, sub_stream="fusion")
        concatenated = self.fc1(concatenated)
        concatenated = self.fc2(concatenated)
        concatenated = self.relu(concatenated)

        return concatenated

    # ------------------------------------------------------------------------------------------------------------------
    # -------------------------------------- M U L T I H E A D A T T E N T I O N ---------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def multi_head_attention(self, x: torch.Tensor, sub_stream: str):
        """
        This function implements the multi-head attention

        Args:
            x: Input tensor
            sub_stream: type of sub stream

        Returns:
            Attention module output tensor
        """

        if len(x.shape) == 2:
            x = x.unsqueeze(2).unsqueeze(3)

        batch_size, _, height, width = x.size()
        x = x.view(batch_size, height * width, -1)
        x = x.permute(1, 0, 2)
        queries = x
        keys = x
        values = x

        multi_head_module = self.multi_head_modules.get(sub_stream)
        if multi_head_module is None:
            raise ValueError("Invalid sub_stream value. I")

        attention_output, _ = multi_head_module(queries, keys, values)
        attention_output = attention_output.permute(1, 0, 2)

        return attention_output.squeeze(1)
