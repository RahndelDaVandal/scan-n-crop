from pathlib import Path
from glob import glob
from os.path import basename

import cv2
import numpy as np
from rich.traceback import install

install()

def get_contours(img):
    # First make the image 1-bit and get contours
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(imgray, 150, 255, 0)

    cv2.imwrite('thresh.jpg', thresh)
    img2, contours, hierarchy = cv2.findContours(thresh, 1, 2)

    # filter contours that are too large or small
    size = get_size(img)
    contours = [cc for cc in contours if contourOK(cc, size)]
    return contours

def get_size(img):
    ih, iw = img.shape[:2]
    return iw * ih

def contourOK(cc, size=1000000):
    x, y, w, h = cv2.boundingRect(cc)
    if w < 50 or h < 50: return False # too narrow or wide is bad
    area = cv2.contourArea(cc)
    return area < (size * 0.5) and area > 200

def find_boundaries(img, contours):
    # margin is the minimum distance from the edges of the image, as a fraction
    ih, iw = img.shape[:2]
    minx = iw
    miny = ih
    maxx = 0
    maxy = 0

    for cc in contours:
        x, y, w, h = cv2.boundingRect(cc)
        if x < minx: minx = x
        if y < miny: miny = y
        if x + w > maxx: maxx = x + w
        if y + h > maxy: maxy = y + h

    return (minx, miny, maxx, maxy)

def crop(img, boundaries):
    minx, miny, maxx, maxy = boundaries
    return img[miny:maxy, minx:maxx]

def process_image(fname):
    img = cv2.imread(fname)
    contours = get_contours(img)
    #cv2.drawContours(img, contours, -1, (0,255,0)) # draws contours, good for debugging
    bounds = find_boundaries(img, contours)
    cropped = crop(img, bounds)
    if get_size(cropped) < 400: return # too small
    cv2.imwrite('cropped/' + basename(fname), cropped)

# process_image('pic.jpg')

# img_path = Path(__file__).parent.parent / 'imgs' / 'middle.JPG'
img_path = Path(__file__).parent.parent / 'imgs' / 'crooked.JPG'

img = cv2.imread(str(img_path))
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(img_gray, 150, 255, 0)
cv2.imwrite('thresh.jpg', thresh)
contours, hierarchy = cv2.findContours(thresh, 1, 2)
size = get_size(img)
contours = [cc for cc in contours if contourOK(cc, size)]
bounds = find_boundaries(img, contours)
cropped = crop(img, bounds)
if not get_size(cropped) < 400:
    cv2.imwrite('cropped.JPG', cropped)
else:
    print("Too Small")