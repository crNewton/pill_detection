import gc
import logging
import matplotlib.pyplot as plt
import os
import pandas as pd
import re
import time
import torch

from datetime import datetime
from functools import wraps
from PIL import Image
from torch import Tensor
from typing import List, Union
from tqdm import tqdm

from config.logger_setup import setup_logger

setup_logger()


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------  D I C E   C O E F F ------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def dice_coefficient(input_tensor: Tensor, target: Tensor, reduce_batch_first: bool = False, epsilon: float = 1e-6) \
        -> Tensor:
    """
    Average of Dice coefficient for all batches, or for a single mask

    :param input_tensor: The input tensor with shape (batch_size, num_classes, height, width).
    :param target: The target tensor with shape (batch_size, num_classes, height, width)
    :param reduce_batch_first: A flag indicating whether to reduce the batch dimension first before computing the
    Dice coefficient. Default is False.
    :param epsilon: A small value to prevent division by zero. Default is 1e-6.
    :return: The Dice coefficient computed for each batch or for a single mask, depending on the reduce_batch_first
    flag. If reduce_batch_first is True, the returned tensor has shape (num_classes,).
    If reduce_batch_first is False, the returned tensor has shape (batch_size, num_classes)
    """

    assert input_tensor.size() == target.size()
    assert input_tensor.dim() == 3 or not reduce_batch_first

    sum_dim = (-1, -2) if input_tensor.dim() == 2 or not reduce_batch_first else (-1, -2, -3)

    inter = 2 * (input_tensor * target).sum(dim=sum_dim)
    sets_sum = input_tensor.sum(dim=sum_dim) + target.sum(dim=sum_dim)
    sets_sum = torch.where(sets_sum == 0, inter, sets_sum)

    dice = (inter + epsilon) / (sets_sum + epsilon)
    return dice.mean()


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ M C L A S S   D I C E   C O E F F -----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def multiclass_dice_coefficient(input_tensor: Tensor, target: Tensor, reduce_batch_first: bool = False,
                                epsilon: float = 1e-6):
    """
    Calculate the average Dice coefficient for all classes in a multi-class segmentation task.

    :param input_tensor: The input tensor with shape [batch_size, num_classes, height, width]
    :param target: The target tensor with shape [batch_size, num_classes, height, width].
    :param reduce_batch_first: Whether to reduce the batch size before calculating the Dice coefficient.
    :param epsilon: A small value added to the denominator to avoid division by zero.
    :return: The average Dice coefficient for all classes.
    """

    return dice_coefficient(input_tensor.flatten(0, 1), target.flatten(0, 1), reduce_batch_first, epsilon)


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ D I C E   L O S S ---------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def dice_loss(input_tensor: Tensor, target: Tensor, multiclass: bool = False) -> float:
    """
    Dice loss (objective to minimize) between 0 and 1

    :param input_tensor: a tensor representing the predicted mask, of shape (batch_size, num_classes, height, width)
    :param target: a tensor representing the ground truth mask, of shape (batch_size, num_classes, height, width)
    :param multiclass: a boolean flag that indicates whether the input and target tensors represent a multiclass
    segmentation task, where each pixel can belong to one of several classes
    :return: a scalar tensor representing the Dice loss between the input and target tensors, which is a value between
    0 and 1.
    """

    fn = multiclass_dice_coefficient if multiclass else dice_coefficient
    return 1 - fn(input_tensor, target, reduce_batch_first=True)


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- N U M E R I C A L   S O R T --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def numerical_sort(value: str) -> List[Union[str, int]]:
    """
    Sort numerical values in a string in a way that ensures numerical values are sorted correctly.

    :param value: The input string.
    :return: A list of strings and integers sorted by numerical value.
    """

    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- C R E A T E   T I M E S T A M P ------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def create_timestamp() -> str:
    """
    Creates a timestamp in the format of '%Y-%m-%d_%H-%M-%S', representing the current date and time.

    :return: The timestamp string.
    """

    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------- F I N D   L A T E S T   F I L E   I N   L A T E S T   D I R E C T O R Y ----------------------
# ----------------------------------------------------------------------------------------------------------------------
def find_latest_file_in_latest_directory(path: str) -> str:
    """
    Finds the latest file in the latest directory within the given path.

    :param path: str, the path to the directory where we should look for the latest file
    :return: str, the path to the latest file
    :raise: when no directories or files found
    """

    # Get a list of all directories in the given path
    dirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    if not dirs:
        raise ValueError(f"No directories found in {path}")

    # Sort directories by creation time (newest first)
    dirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Get the latest directory
    latest_dir = dirs[0]

    # Get a list of all files in the latest directory
    files = [os.path.join(latest_dir, f) for f in os.listdir(latest_dir) if
             os.path.isfile(os.path.join(latest_dir, f))]

    if not files:
        raise ValueError(f"No files found in {latest_dir}")

    # Sort files by creation time (newest first)
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Get the latest file
    latest_file = files[0]

    logging.info(f"The latest file is {latest_file}")
    return latest_file


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------- P L O T   R E F   Q U E R Y   I M G S ---------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def plot_ref_query_images(indices: list[int], q_images_path: list[str], r_images_path: list[str], gt: list[str],
                          pred_cs: list[str], out_path: str) -> None:
    """
    Plots the reference and query images with their corresponding ground truth and predicted class labels.

    :param indices: list of indices representing the matched reference images for each query image
    :param q_images_path: list of file paths to query images
    :param r_images_path: list of file paths to reference images
    :param gt: list of ground truth class labels for each query image
    :param pred_cs: list of predicted class labels for each query image
    :param out_path: stream or fusion network path
    :return: None
    """

    new_list = [i for i in range(len(indices))]

    for idx, (i, j, k, l) in tqdm(enumerate(zip(indices, new_list, gt, pred_cs)), total=len(new_list),
                                  desc="Plotting ref and query images"):
        img_path_query = q_images_path[j]
        img_query = Image.open(img_path_query)

        img_path_ref = r_images_path[int(i)]
        img_ref = Image.open(img_path_ref)

        plt.figure()
        f, ax = plt.subplots(1, 2)
        ax[0].imshow(img_query)
        ax[0].set_title(k + "_query")
        ax[1].imshow(img_ref)
        ax[1].set_title(l + "_ref")

        output_path = os.path.join(out_path, str(idx) + ".png")
        plt.savefig(output_path)
        plt.close()

        plt.close("all")
        plt.close()
        gc.collect()


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------- P R I N T   N E T W O R K   C O N F I G --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def print_network_config(cfg):
    """

    :param cfg:
    :return:
    """

    df = pd.DataFrame.from_dict(vars(cfg), orient='index', columns=['value'])
    logging.info("Parameters of the selected %s:", cfg.type_of_net)
    logging.info(df)


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------- U S E   G P U   I F   A V A I L A B L E --------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def use_gpu_if_available() -> torch.device:
    """
    Provides information about the currently available GPUs and returns a torch device for training and inference.

    :return: A torch device for either "cuda" or "cpu".
    """

    cuda_info = {
        'CUDA Available': [torch.cuda.is_available()],
        'CUDA Device Count': [torch.cuda.device_count()],
        'Current CUDA Device': [torch.cuda.current_device()],
        'CUDA Device Name': [torch.cuda.get_device_name(0)]
    }

    df = pd.DataFrame(cuda_info)
    logging.info(df)

    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------- M E A S U R E   E X E C U T I O N   T I M E ------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def measure_execution_time(func):
    """
    Decorator to measure the execution time.

    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time} seconds")
        return result
    return wrapper
