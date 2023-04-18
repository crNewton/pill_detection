import numpy as np
import os
import torch
import torch.nn as nn

from tqdm import tqdm
from torch.utils.data import DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter
from torchsummary import summary

from config import ConfigFusionNetwork
from const import CONST
from fusion_network import FusionNet
from fusion_dataset_loader import FusionDataset
from utils.utils import create_timestamp, find_latest_file

cfg = ConfigFusionNetwork().parse()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++ T R A I N   M O D E L +++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TrainFusionNet:
    def __init__(self):
        # Create time stamp
        self.timestamp = create_timestamp()

        # Select the GPU if possibly
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        list_of_channels_con_tex = [1, 32, 48, 64, 128, 192, 256]
        list_of_channels_rgb = [3, 64, 96, 128, 256, 384, 512]

        # Load datasets using FusionDataset
        dataset = FusionDataset("C:/Users/ricsi/Documents/project/storage/IVM/images")
        train_size = int(cfg.train_split * len(dataset))
        valid_size = len(dataset) - train_size
        print(f"Size of the train set: {train_size}, size of the validation set: {valid_size}")
        train_dataset, valid_dataset = random_split(dataset, [train_size, valid_size])
        self.train_data_loader = DataLoader(train_dataset, batch_size=cfg.batch_size, shuffle=True)
        self.valid_data_loader = DataLoader(valid_dataset, batch_size=cfg.batch_size, shuffle=True)

        # # Initialize the fusion network
        self.model = FusionNet()

        # Load the saved state dictionaries of the stream networks
        stream_con_state_dict = (torch.load(find_latest_file(CONST.dir_stream_contour_model_weights)))
        stream_rgb_state_dict = (torch.load(find_latest_file(CONST.dir_stream_rgb_model_weights)))
        stream_tex_state_dict = (torch.load(find_latest_file(CONST.dir_stream_texture_model_weights)))

        # Update the state dictionaries of the fusion network's stream networks
        self.model.contour_network.load_state_dict(stream_con_state_dict)
        self.model.rgb_network.load_state_dict(stream_rgb_state_dict)
        self.model.texture_network.load_state_dict(stream_tex_state_dict)

        # Freeze the weights of the stream networks
        for param in self.model.contour_network.parameters():
            param.requires_grad = False
        for param in self.model.rgb_network.parameters():
            param.requires_grad = False
        for param in self.model.texture_network.parameters():
            param.requires_grad = False

        # Load model and upload it to the GPU
        self.model.to(self.device)
        summary(self.model, input_size=[(list_of_channels_con_tex[0], cfg.img_size, cfg.img_size),
                                        (list_of_channels_rgb[0], cfg.img_size, cfg.img_size),
                                        (list_of_channels_con_tex[0], cfg.img_size, cfg.img_size)])

        # Specify loss function
        self.criterion = nn.TripletMarginLoss(margin=cfg.margin)

        # Specify optimizer
        self.optimizer = torch.optim.SGD(list(self.model.fc1.parameters()) + list(self.model.fc2.parameters()),
                                         lr=cfg.learning_rate, weight_decay=cfg.weight_decay)
        # Tensorboard
        tensorboard_log_dir = os.path.join(CONST.dir_fusion_net_logs, self.timestamp)
        if not os.path.exists(tensorboard_log_dir):
            os.makedirs(tensorboard_log_dir)

        self.writer = SummaryWriter(log_dir=tensorboard_log_dir)

        # Create save path
        self.save_path = os.path.join(CONST.dir_fusion_net_weights, self.timestamp)
        os.makedirs(self.save_path, exist_ok=True)

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------ F I T -----------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def fit(self):
        # to track the training loss as the model trains
        train_losses = []

        # to track the validation loss as the model trains
        valid_losses = []

        for epoch in tqdm(range(cfg.epochs), desc="Epochs"):
            for a_rgb, a_con, a_tex, p_rgb, p_con, p_tex, n_rgb, n_con, n_tex in tqdm(self.train_data_loader,
                                                                                      total=len(self.train_data_loader),
                                                                                      desc="Training"):
                anchor_rgb = a_rgb.to(self.device)
                positive_rgb = p_rgb.to(self.device)
                negative_rgb = n_rgb.to(self.device)

                anchor_contour = a_con.to(self.device)
                positive_contour = p_con.to(self.device)
                negative_contour = n_con.to(self.device)

                anchor_texture = a_tex.to(self.device)
                positive_texture = p_tex.to(self.device)
                negative_texture = n_tex.to(self.device)

                self.optimizer.zero_grad()

                # Forward pass
                anchor_out = self.model(anchor_contour, anchor_rgb, anchor_texture)
                positive_out = self.model(positive_contour, positive_rgb, positive_texture)
                negative_out = self.model(negative_contour, negative_rgb, negative_texture)

                # Compute triplet loss
                t_loss = self.criterion(anchor_out, positive_out, negative_out)

                # Backward pass
                t_loss.backward()
                self.optimizer.step()

                # Accumulate loss
                train_losses.append(t_loss.item())

            # Validation loop
            with torch.no_grad():
                for a_rgb, a_con, a_tex, p_rgb, p_con, p_tex, n_rgb, n_con, n_tex in \
                        tqdm(self.valid_data_loader, total=len(self.valid_data_loader), desc="Validation"):
                    anchor_rgb = a_rgb.to(self.device)
                    positive_rgb = p_rgb.to(self.device)
                    negative_rgb = n_rgb.to(self.device)

                    anchor_contour = a_con.to(self.device)
                    positive_contour = p_con.to(self.device)
                    negative_contour = n_con.to(self.device)

                    anchor_texture = a_tex.to(self.device)
                    positive_texture = p_tex.to(self.device)
                    negative_texture = n_tex.to(self.device)

                    self.optimizer.zero_grad()

                    # Forward pass
                    anchor_out = self.model(anchor_contour, anchor_rgb, anchor_texture)
                    positive_out = self.model(positive_contour, positive_rgb, positive_texture)
                    negative_out = self.model(negative_contour, negative_rgb, negative_texture)

                    # Compute triplet loss
                    v_loss = self.criterion(anchor_out, positive_out, negative_out)
                    valid_losses.append(v_loss.item())

            # Print loss for epoch
            train_loss = np.average(train_losses)
            valid_loss = np.average(valid_losses)
            print(f'train_loss: {train_loss:.5f} ' + f'valid_loss: {valid_loss:.5f}')

            # Record to tensorboard
            self.writer.add_scalars("Loss", {"train": train_loss, "validation": valid_loss}, epoch)

            # Clear lists to track next epoch
            train_losses.clear()
            valid_losses.clear()

            # Save the model and weights
            if cfg.save and epoch % cfg.save_freq == 0:
                filename = os.path.join(self.save_path, "epoch_" + (str(epoch) + ".pt"))
                torch.save(self.model.state_dict(), filename)

        # Close and flush SummaryWriter
        self.writer.close()
        self.writer.flush()


if __name__ == "__main__":
    try:
        tm = TrainFusionNet()
        tm.fit()
    except KeyboardInterrupt as kbe:
        print(kbe)
