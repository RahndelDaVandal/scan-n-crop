# scan_n_crop.app
from pathlib import Path
import cv2 as cv
import numpy as np
from cropper import Cropper


class App:
    def __init__(self) -> None:
        self._cropper = None

    @property
    def cropper(self) -> Cropper:
        return self._cropper

    @cropper.setter
    def cropper(self, cropper: Cropper) -> None:
        self._cropper = cropper

    @staticmethod
    def _load(file_path: str) -> np.ndarray:
        if not Path(file_path).is_file():
            raise FileExistsError

        return cv.imread(str(file_path), 1)

    @staticmethod
    def _generate_cropped_file_path(original_path: str) -> str:
        original = Path(original_path)
        dir = original.parent
        file_name = str(original.stem + "_CROPPED" + original.suffix)
        return str(dir / file_name)

    @staticmethod
    def _save(file_path: str, img: np.ndarray) -> None:
        cv.imwrite(str(file_path), img)

    def crop(self, file_path: str) -> None:
        if self._cropper is None:
            raise ValueError('app.cropper is None')

        img = self._load(file_path)
        cropped_img = self._cropper.crop(img)
        cropped_img_name = self._generate_cropped_file_path(file_path)
        self._save(cropped_img_name, cropped_img)
