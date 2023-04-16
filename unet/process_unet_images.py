import cv2
import numpy as np
import os

from concurrent.futures import ThreadPoolExecutor, wait
from glob import glob
from tqdm import tqdm
from typing import Tuple

from const import CONST
from utils.utils import numerical_sort, create_label_dirs


class ProcessUnetImages:
    def __init__(self, operation: str = "test"):
        self.path_to_images = self.path_selector(operation)

    @staticmethod
    def path_selector(operation):
        """
        Selects the correct directory paths based on the given operation string.

        :param operation: A string indicating the operation mode (train or test).
        :return: A dictionary containing directory paths for images, masks, and other related files.
        :raises ValueError: If the operation string is not "train" or "test".
        """

        if operation.lower() == "train":
            path_to_images = {
                "images": CONST.dir_train_images,
                "masks": CONST.dir_train_masks,
                "rgb": CONST.dir_bounding_box,
                "contour": CONST.dir_contour,
                "texture": CONST.dir_texture
            }
        elif operation.lower() == "test":
            path_to_images = {
                "images": CONST.dir_test_images,
                "masks": CONST.dir_test_mask,
                "rgb": CONST.dir_query_rgb,
                "contour": CONST.dir_query_contour,
                "texture": CONST.dir_query_texture
            }
        else:
            raise ValueError("Wrong operation!")

        return path_to_images

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------- D R A W   B O U N D I N G   B O X ---------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def draw_bounding_box(in_img: np.ndarray, seg_map: np.ndarray, output_path: str) -> None:
        """
        Draws bounding box over medicines. It draws only the biggest bounding box, small ones are terminated.
        After that it crops out the bounding box's content.

        :param in_img: input testing image
        :param seg_map: output of the unet for the input testing image
        :param output_path: where the file should be saved
        :return: None
        """

        ret, thresh = cv2.threshold(seg_map, 0, 255, cv2.THRESH_BINARY)
        n_objects, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8, ltype=cv2.CV_32S)

        max_area = 0
        max_x, max_y, max_w, max_h = None, None, None, None

        for i in range(1, n_objects):
            x, y, w, h, area = stats[i]
            if area > 200 and area > max_area:
                max_x, max_y, max_w, max_h = x, y, w, h
                max_area = area

        if max_area > 0:
            center_x = max_x + max_w / 2
            center_y = max_y + max_h / 2
            side_length = max(max_w, max_h)
            square_x = int(center_x - side_length / 2)
            square_y = int(center_y - side_length / 2)
            obj = in_img[square_y:square_y + side_length, square_x:square_x + side_length]
            cv2.imwrite(output_path, obj)

    # ------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------- P R O C E S S   I M A G E -------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def process_image(self, image_paths: Tuple[str, str]) -> None:
        """
        Processes a single image by reading in the color and mask images, drawing the bounding box, and saving the
        result.
        :param image_paths: tuple of paths to the color and mask images
        :return: None
        """

        color_path, mask_path = image_paths
        output_name = os.path.basename(color_path)
        output_file = os.path.join(self.path_to_images.get("rgb"), output_name)
        c_imgs = cv2.imread(color_path, 1)
        m_imgs = cv2.imread(mask_path, 0)
        self.draw_bounding_box(c_imgs, m_imgs, output_file)

    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------- S A V E   B O U N D I N G   B O X   I M G S ----------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def save_bounding_box_images(self) -> None:
        """
        Reads in the images, draws the bounding box, and saves the images in parallel.
        :return: None
        """

        # Read in all color and mask image paths
        color_images = sorted(glob(self.path_to_images.get("images") + "/*.png"))
        mask_images = sorted(glob(self.path_to_images.get("masks") + "/*.png"))

        # Process the images in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            list(tqdm(executor.map(self.process_image, zip(color_images, mask_images)), total=len(color_images),
                      desc="Bounding box"))

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------ C R E A T E   C O N T O U R   I M A G E S -----------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_contour_images(args):
        """
        Applies edge detection on an input image and saves the resulting edge map.

        :param args: Tuple containing:
            - cropped_image (numpy.ndarray): The input image to apply edge detection on.
            - output_path (str): The path to save the output edge map.
            - kernel_size (int): The size of the kernel used in median blur.
            - canny_low_thr (int): The lower threshold for Canny edge detection.
            - canny_high_thr (int): The higher threshold for Canny edge detection.
        :return: None
        """

        cropped_image, output_path, kernel_size, canny_low_thr, canny_high_thr = args
        blured_images = cv2.medianBlur(cropped_image, kernel_size, 0)
        edges = cv2.Canny(blured_images, canny_low_thr, canny_high_thr)
        cv2.imwrite(output_path, edges)

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------- S A V E   C O N T O U R   I M G S ---------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def save_contour_images(self):
        """
        Loads RGB images from the designated directory and applies Canny edge detection algorithm to extract contours
        for each image. The resulting images are saved in a new directory designated for contour images.

        :return: None
        """

        contour_images = sorted(glob(self.path_to_images.get("rgb") + "/*.png"), key=numerical_sort)
        args_list = []

        for img_path in tqdm(contour_images, desc="Contour images"):
            output_name = "contour_" + img_path.split("\\")[2]
            output_file = (os.path.join(self.path_to_images.get("contour"), output_name))
            bbox_imgs = cv2.imread(img_path, 0)
            args_list.append((bbox_imgs, output_file, 7, 10, 50))

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_contour_images, args) for args in args_list]
            wait(futures)

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------ C R E A T E   T E X T U R E   I M A G E S -----------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_texture_images(args):
        """
        Given a cropped input image, this method applies a Gaussian blur, subtracts the blurred image from the original,
        normalizes the resulting image intensities between 0 and 255, and saves the resulting texture image to a
        given path.
        :param args: A tuple containing the following elements:
            - cropped_image: A numpy array representing the cropped input image
            - output_path: A string representing the path to save the output texture image
            - kernel_size: An integer representing the size of the Gaussian blur kernel
        :return: None
        """

        cropped_image, output_path, kernel_size = args
        blured_image = cv2.GaussianBlur(cropped_image, kernel_size, 0)
        sub_img = cv2.subtract(cropped_image, blured_image)
        min_val = sub_img.min()
        max_val = sub_img.max()
        sub_img = (sub_img - min_val) * (255.0 / (max_val - min_val))
        sub_img = sub_img.astype(np.uint8)
        cv2.imwrite(output_path, sub_img)

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------- S A V E   T E X T U R E   I M G S ---------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def save_texture_images(self):
        """
        Save texture images using Gaussian Blur filter.

        :return: None
        """

        bbox_images = sorted(glob(self.path_to_images.get("rgb") + "/*.png"), key=numerical_sort)
        args_list = []

        for img_path in tqdm(bbox_images, desc="Texture images"):
            output_name = "texture_" + img_path.split("\\")[2]
            output_file = (os.path.join(self.path_to_images.get("texture"), output_name))
            bbox_imgs = cv2.imread(img_path, 0)
            args_list.append((bbox_imgs, output_file, (7, 7)))

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_texture_images, args) for args in args_list]
            wait(futures)

    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------- M A I N ----------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def main(self):
        """
        Executes the functions to create the images.

        :return: None
        """

        self.save_bounding_box_images()
        self.save_contour_images()
        self.save_texture_images()
        create_label_dirs(rgb_path=self.path_to_images.get("rgb"),
                          contour_path=self.path_to_images.get("contour"),
                          texture_path=self.path_to_images.get("texture"))


if __name__ == "__main__":
    proc_unet_imgs = ProcessUnetImages(operation="Test")
    proc_unet_imgs.main()
