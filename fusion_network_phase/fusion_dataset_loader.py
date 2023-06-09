import numpy as np
import os
import torch

from PIL import Image
from torch.utils.data import Dataset
from torchvision.transforms import transforms
from typing import Tuple

from config.const import IMAGES_PATH


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++ F U S I O N D A T A S E T +++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FusionDataset(Dataset):
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------- __ I N I T __ --------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self) -> None:
        """
        This is the __init__ function of the dataset loader class.

        :return: None
        """

        self.label_to_indices = None
        self.labels = None

        # Transforms for each dataset
        self.rgb_transform = transforms.Compose([
            transforms.Resize(128),
            transforms.CenterCrop(128),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])
        self.texture_transform = transforms.Compose([
            transforms.Resize(128),
            transforms.CenterCrop(128),
            transforms.Grayscale(),
            transforms.ToTensor()
        ])
        self.contour_transform = transforms.Compose([
            transforms.Resize(128),
            transforms.CenterCrop(128),
            transforms.Grayscale(),
            transforms.ToTensor()
        ])
        self.lbp_transform = transforms.Compose([
            transforms.Resize(128),
            transforms.CenterCrop(128),
            transforms.Grayscale(),
            transforms.ToTensor()
        ])

        # Load datasets
        self.rgb_dataset = self.load_dataset(IMAGES_PATH.get_data_path("rgb_hardest"))
        self.texture_dataset = self.load_dataset(IMAGES_PATH.get_data_path("texture_hardest"))
        self.contour_dataset = self.load_dataset(IMAGES_PATH.get_data_path("contour_hardest"))
        self.lbp_dataset = self.load_dataset(IMAGES_PATH.get_data_path("lbp_hardest"))
        self.labels_set = set(label for _, label in self.rgb_dataset)
        self.prepare_labels()

    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------- __ G E T I T E M __ ----------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor,
                                               torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor,
                                               torch.Tensor, torch.Tensor]:
        """
        This is the __getitem__ method of a dataset loader class. Given an index, it loads the corresponding images from
        three different datasets (RGB, texture, contour, LBP), and applies some data augmentation (transforms) to each
        image. It then returns a tuple of twelve images.

        :param index: An integer representing the index of the sample to retrieve from the dataset.
        :return: A tuple of 12 elements, where each element corresponds to an image with a specific transformation.
        """

        # Load corresponding images from all datasets
        rgb_anchor_img_path, anchor_label = self.rgb_dataset[index]
        texture_anchor_img_path, _ = self.texture_dataset[index]
        contour_anchor_img_path, _ = self.contour_dataset[index]
        lbp_anchor_img_path, _ = self.lbp_dataset[index]

        # Load positive sample from the same class as anchor
        positive_index = index
        while positive_index == index:
            positive_index = np.random.choice(self.label_to_indices[anchor_label])
        rgb_positive_img_path, _ = self.rgb_dataset[positive_index]
        texture_positive_img_path, _ = self.texture_dataset[positive_index]
        contour_positive_img_path, _ = self.contour_dataset[positive_index]
        lbp_positive_img_path, _ = self.lbp_dataset[positive_index]

        # Load negative sample from a different class
        negative_label = np.random.choice(list(self.labels_set - {anchor_label}))
        negative_index = np.random.choice(self.label_to_indices[negative_label])
        rgb_negative_img_path, _ = self.rgb_dataset[negative_index]
        texture_negative_img_path, _ = self.texture_dataset[negative_index]
        contour_negative_img_path, _ = self.contour_dataset[negative_index]
        lbp_negative_img_path, _ = self.lbp_dataset[negative_index]

        # Load images and apply transforms
        rgb_anchor_img = Image.open(rgb_anchor_img_path)
        rgb_positive_img = Image.open(rgb_positive_img_path)
        rgb_negative_img = Image.open(rgb_negative_img_path)

        texture_anchor_img = Image.open(texture_anchor_img_path)
        texture_positive_img = Image.open(texture_positive_img_path)
        texture_negative_img = Image.open(texture_negative_img_path)

        contour_anchor_img = Image.open(contour_anchor_img_path)
        contour_positive_img = Image.open(contour_positive_img_path)
        contour_negative_img = Image.open(contour_negative_img_path)

        lbp_anchor_img = Image.open(lbp_anchor_img_path)
        lbp_positive_img = Image.open(lbp_positive_img_path)
        lbp_negative_img = Image.open(lbp_negative_img_path)

        rgb_anchor_img = self.rgb_transform(rgb_anchor_img)
        rgb_positive_img = self.rgb_transform(rgb_positive_img)
        rgb_negative_img = self.rgb_transform(rgb_negative_img)

        texture_anchor_img = self.texture_transform(texture_anchor_img)
        texture_positive_img = self.texture_transform(texture_positive_img)
        texture_negative_img = self.texture_transform(texture_negative_img)

        contour_anchor_img = self.contour_transform(contour_anchor_img)
        contour_positive_img = self.contour_transform(contour_positive_img)
        contour_negative_img = self.contour_transform(contour_negative_img)

        lbp_anchor_img = self.lbp_transform(lbp_anchor_img)
        lbp_positive_img = self.lbp_transform(lbp_positive_img)
        lbp_negative_img = self.lbp_transform(lbp_negative_img)

        return (rgb_anchor_img, texture_anchor_img, contour_anchor_img, lbp_anchor_img,
                rgb_positive_img, texture_positive_img, contour_positive_img, lbp_positive_img,
                rgb_negative_img, texture_negative_img, contour_negative_img,lbp_negative_img)

    # ------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------- __ L E N __ --------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def __len__(self):
        """
        This is the __len__ method of a dataset loader class.

        :return:
        """

        return len(self.rgb_dataset)

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------- L O A D   T H E   D A T A S E T -----------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def load_dataset(self, dataset_name: str) -> list:
        """
        Loads a dataset with the specified name from the dataset directory and returns a list of image paths and their
        corresponding labels, as well as storing the labels separately in the 'labels' attribute of the class instance.

        :param dataset_name: name of the dataset to be loaded
        :return: a list of tuples containing image paths and their corresponding labels, extracted from the specified
        dataset directory. The labels are also stored separately in the class attribute 'labels'.
        """

        dataset = []
        labels = []

        for label_name in os.listdir(dataset_name):
            label_path = os.path.join(dataset_name, label_name)
            if not os.path.isdir(label_path):
                continue
            label = label_name
            for image_name in os.listdir(label_path):
                image_path = os.path.join(label_path, image_name)
                dataset.append((image_path, label))
                labels.append(label)
        self.labels = labels

        return dataset

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------- P R E P A R E   L A B E L S ------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def prepare_labels(self) -> None:
        """
        # Initialize dictionary that maps each label to corresponding indices in dataset

        :return: None
        """

        self.label_to_indices = {label: [] for label in self.labels_set}
        for i in range(len(self.labels)):
            label = self.labels[i]
            self.label_to_indices[label].append(i)
