# cropping_strategies.py
from dataclasses import dataclass, field
import numpy as np
import cv2 as cv


@dataclass
class SinglePhotoScanCropper:
    _scan: np.ndarray = field(repr=False, default=None)
    _scan_grayscale: np.ndarray = field(repr=False, default=None)
    _scan_contours: tuple = field(repr=False, default=None)
    _photo_contour: np.ndarray = field(repr=False, default=None)
    _bounding_box: np.ndarray = field(repr=False, default=None)
    _photo: np.ndarray = field(repr=False, default=None)

    def _reset_class_values(self) -> None:
        self._scan = None
        self._scan_grayscale = None
        self._scan_contours = None
        self._photo_contour = None
        self._bounding_box = None
        self._photo = None

    def _convert_to_grayscale(self) -> None:
        self._scan_grayscale = cv.cvtColor(self._scan, cv.COLOR_BGR2GRAY)

    def _get_scan_contours(self) -> None:
        # TODO - Check actual return type is a tuple
        _, thresh = cv.threshold(self._scan_grayscale, 127, 255, 0)
        self._scan_contours = cv.findContours(
            thresh,
            cv.RETR_TREE,
            cv.CHAIN_APPROX_SIMPLE,
        )

    def _find_photo_contour(self) -> None:
        contours, hierarchy = self._scan_contours
        photo = []
        for idx, val in enumerate(hierarchy[0]):
            _next, _prev, _child, _parent = val
            if _next == -1 and _parent == 0 and _child != -1:
                photo.append(contours[idx])
        if len(photo) > 1:
            raise ValueError("scan has more than one photo")
        self._photo_contour = photo[0]

    def _create_photo_bounding_box(self) -> None:
        rect = cv.minAreaRect(self._photo_contour[0])
        self._bounding_box = np.int0(cv.boxPoints(rect))

    def _crop_photo(self) -> None:
        center, size, angle = cv.minAreaRect(self._photo_contour)
        center, size = tuple(map(int, center)), tuple(map(int, size))
        # height, width = self._scan.shape[:2]
        height, width = (self._scan.shape[1], self._scan.shape[0])
        M = cv.getRotationMatrix2D(center, -angle, 1)
        scan_rotated = cv.warpAffine(self._scan, M, (width, height))
        cropped_photo = cv.getRectSubPix(scan_rotated, size, center)
        self._photo = cropped_photo

    def crop(self, scan: np.ndarray) -> list[np.ndarray]:
        self._reset_class_values()
        # TODO - scan validation - check scan.shape
        # TODO - do I need to worry about BGR vs RGB?
        # TODO - do I need copy for original scan protection?
        self._scan = scan.copy()
        self._convert_to_grayscale()
        self._get_scan_contours()
        self._find_photo_contour()
        # self._create_photo_bounding_box()
        self._crop_photo()
        return self._photo
