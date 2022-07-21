# cropping_strategies.py

import numpy as np

from img_cropper import ImgCropper


class cvSinglePhotoContourCrop(ImgCropper):
    def crop(self, img: np.ndarray) -> list[np.ndarray]:
        # Crop image using opencv contours
        pass
