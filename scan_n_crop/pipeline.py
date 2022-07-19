from pathlib import Path
import statistics

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img_path = Path().resolve().parent / 'imgs' / 'crooked.JPG'
img_path.is_file()

def img_import(file_path: str) -> tuple:
    #OpenCV uses BGR not RGB
    img = cv.imread(str(img_path), 1)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return (img, img_gray)
    
def img_show(img: np.ndarray) -> None:
    plt.figure(figsize=(20,10))
    if len(img.shape) == 2:
        plt.imshow(img, cmap="gray")
    else:
        plt.imshow(img[...,::-1])

def get_contours(img: np.ndarray) -> np.ndarray:
    if len(img.shape) > 2:
        raise ValueError('Length of img.shape is greater than 2.\nImage must be a 2D numpy.ndarray.\nTry converting to grayscale?')
    
    ret, thresh = cv.threshold(img, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy

def get_photo_contour(contours: tuple, hierarchy: np.ndarray) -> np.ndarray:
    photos = []
    for idx, val in enumerate(hierarchy[0]):
        _next, _prev, _child, _parent = val
        if _next == -1 and _parent == 0 and _child != -1:
            photos.append(contours[idx])
            
    # TODO - Add code to handle if there are multiple photos in a single img/scan
    if len(photos) > 1:
        print('photos length is greater than 1.... possibly more than one photo? multiple photos code not implimented yet')
        return
    else:
        return photos

def deskew(img: np.ndarray, photo_contour: np.ndarray) -> np.ndarray:
    rect = cv.minAreaRect(photo_contour[0])
    angle = rect[-1]
    h, w = img.shape[:2]
    center = (w / 2, h / 2)
    M = cv.getRotationMatrix2D(center, angle-360, 1.0)
    deskewed = cv.warpAffine(img, M, (h, w))
    return deskewed
    
def get_photo_boundies(photo_contour: np.ndarray):
    rect = cv.minAreaRect(photo_contour[0])
    print(rect)
    print(type(rect))
    angle = rect[-1]
    box = np.int0(cv.boxPoints(rect))
    return box

def crop_rect(img: np.ndarray, rect: tuple) -> np.ndarray:
    center, size, angle = rect
    center, size = tuple(map(int, center)), tuple(map(int, size))
    height, width = img.shape[:2]
    M = cv.getRotationMatrix2D(center, angle, 1)
    img_rot = cv.warpAffine(img, M, (width, height))
    img_crop = cv.getRectSubPix(img_rot, size, center)

    return img_crop, img_rot
    
img, img_gray = img_import(img_path)
contours, hierarchy = get_contours(img_gray)
photo = get_photo_contour(contours, hierarchy)
rect = cv.minAreaRect(photo[0])
img_crop, img_rot = crop_rect(img, rect)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(24, 12))

ax[0].imshow(img[...,::-1])
ax[0].set_title('original', fontsize=20)

ax[1].imshow(img_rot[...,::-1])
ax[1].set_title('rotated', fontsize=20)

ax[2].imshow(img_crop[...,::-1])
ax[2].set_title('cropped', fontsize=20)

fig.tight_layout()
