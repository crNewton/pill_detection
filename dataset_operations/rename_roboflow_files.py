"""
File: rename_roboflow_files.py
Author: Richárd Rádli
E-mail: radli.richard@mik.uni-pannon.hu
Date: May 23, 2023

Description: Roboflow tends to add name extensions to image files, also, it converts images to .jpg format. This program
chops off the name extensions, and converts back the files to .png files.
"""

import os

from glob import glob
from PIL import Image
from tqdm import tqdm

from config.const import DATASET_PATH


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- R E N A M E   F I L E S -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def rename_files(images_dir: str, labels_dir: str) -> None:
    """
    This function renames the files, generated by Roboflow. Cuts the addon names of the files, and changes the name of
    the extensions to .png and .txt.
    :param images_dir: Path to the image files.
    :param labels_dir: Path to the text files.
    :return: None
    """

    images = sorted(glob(images_dir + "/*.jpg"))
    text = sorted(glob(labels_dir + "/*.txt"))

    existing_files = os.listdir(images_dir)

    for idx, (img, txt) in enumerate(zip(images, text)):
        image_file_name = os.path.basename(img)
        image_file_name = image_file_name.replace("_png", ".png")
        image_file_name = '_'.join(image_file_name.split('.')[:2])
        image_file_name = image_file_name.replace("_png", ".png")

        txt_file_name = os.path.basename(txt)
        txt_file_name = txt_file_name.replace("_png", ".png")
        txt_file_name = '_'.join(txt_file_name.split('.')[:2])
        txt_file_name = txt_file_name.replace("_png", ".txt")

        # Check if the image file name already exists
        original_file_name = image_file_name
        index = 0
        while image_file_name in existing_files:
            index += 1
            image_file_name = "{}_{:03d}.png".format(original_file_name.rsplit('_', 1)[0], index)

        existing_files.append(image_file_name)

        # Rename the corresponding text file
        os.rename(img, os.path.join(images_dir, image_file_name))
        os.rename(txt, os.path.join(labels_dir, txt_file_name))

        # Print the updated file names
        print("Image file:", image_file_name)
        print("Text file:", txt_file_name)


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------- C O N V E R T   I M A G E S   T O   P N G -------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def convert_images_to_png(directory: str) -> None:
    """

    :param directory: Path to the image files.
    :return: None
    """

    image_files = os.listdir(directory)
    for file_name in tqdm(image_files, total=len(image_files), desc="Processing images"):
        if file_name.lower().endswith('.png'):
            image_path = os.path.join(directory, file_name)

            img = Image.open(image_path)
            img = img.convert("RGB")
            img.save(image_path, 'PNG')
            print(f"Converted {file_name}")


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------- M A I N ------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def main() -> None:
    """
    The main function of the file. One can set the directory paths here.
    :return: None
    """

    images_dir = DATASET_PATH.get_data_path("ogyi_v2_unsplitted_images")
    labels_dir = DATASET_PATH.get_data_path("ogyi_v2_unsplitted_labels")

    rename_files(images_dir, labels_dir)
    convert_images_to_png(images_dir)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- __M A I N__ ----------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
