# img_cropper.py

from abc import ABC, abstractmethod

import numpy as np


class ImgCropper(ABC):
    @abstractmethod
    def crop(self, img: np.ndarray) -> list[np.ndarray]:
        pass
