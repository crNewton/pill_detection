import os
import cv2
import numpy as np

from glob import glob
from tqdm import tqdm

from const import CONST


class UnDistortTestImages:
    def __init__(self):
        cam_mtx_np_file = os.path.join(CONST.dir_cam_data, "2023-03-27_12-45-45_undistorted_cam_mtx.npy")
        data = np.load(cam_mtx_np_file, allow_pickle=True)

        self.matrix = data.item()['matrix']
        self.dist_coeff = data.item()['dist_coeff']
        self.undst_matrix = data.item()['undst_matrix']
        self.roi = data.item()['roi']

    @staticmethod
    def crop_image(height, width, crop_size):
        # crop input image
        x_min = int(width / 2 - (crop_size / 2))
        y_min = int(height / 2 - (crop_size / 2))
        x_max = int(width / 2 + (crop_size / 2))
        y_max = int(height / 2 + (crop_size / 2))

        return x_min, y_min, x_max, y_max

    def undistort_images(self):

        loc_of_undis_test_imgs = "C:/Users/ricsi/Desktop/unet_multi_2/"
        loc_to_save = "C:/Users/ricsi/Desktop/unet_multi_undist_2/"
        os.makedirs(loc_to_save, exist_ok=True)
        images = sorted(glob(loc_of_undis_test_imgs + "/*.png"))

        for idx, name in tqdm(enumerate(images), total=len(images)):
            src_img = cv2.imread(name)
            file_name = name.split("\\")[-1]
            save_path = os.path.join(loc_to_save, file_name)
            print(save_path)

            undistorted_image = cv2.undistort(src_img, self.matrix, self.dist_coeff, None, self.undst_matrix)
            x, y, w, h = self.roi
            undistorted_image = undistorted_image[y:y + h, x:x + w]

            x_min, y_min, x_max, y_max = self.crop_image(height=undistorted_image.shape[0],
                                                         width=undistorted_image.shape[1],
                                                         crop_size=800)
            crop_img = undistorted_image[y_min:y_max, x_min:x_max]

            cv2.imwrite(save_path, crop_img)


if __name__ == "__main__":
    undist = UnDistortTestImages()
    undist.undistort_images()
