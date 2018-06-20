import cv2
import math
import numpy as np
from scipy import ndimage
from PIL import Image


def getBestShift(img):
    cy,cx = ndimage.measurements.center_of_mass(img)
    rows,cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)
    return shiftx,shifty


def shift(img,sx,sy):
    rows,cols = img.shape
    M = np.float32([[1,0,sx],[0,1,sy]])
    shifted = cv2.warpAffine(img,M,(cols,rows))
    return shifted


def preprocess(image_name):
    grey = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

    # Invert image, resize to 28x28
    grey = cv2.resize(255-grey, (28, 28))

    # Image binarisation
    (thresh, grey) = cv2.threshold(grey, 128, 255, cv2.THRESH_BINARY)

    if (np.sum(grey) != 0):
        # Crop to bounding box
        while np.sum(grey[0]) == 0:
            grey = grey[1:]

        while np.sum(grey[:,0]) == 0:
            grey = np.delete(grey,0,1)

        while np.sum(grey[-1]) == 0:
            grey = grey[:-1]

        while np.sum(grey[:,-1]) == 0:
            grey = np.delete(grey,-1,1)

        rows, cols = grey.shape

        # Centre 20x20 image to 28x28 using centre of mass
        # Resize outer box to 20x20

        if rows > cols:
          factor = 20.0/rows
          rows = 20
          cols = int(round(cols*factor))
          grey = cv2.resize(grey, (cols, rows))
        else:
          factor = 20.0/cols
          cols = 20
          rows = int(round(rows*factor))
          grey = cv2.resize(grey, (cols, rows))
    
        # Pad image to 28x28
        colsPadding = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
        rowsPadding = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))
        grey = np.lib.pad(grey,(rowsPadding,colsPadding),'constant')
    
        # Shift inner box to centre it by centre of mass
        shiftx,shifty = getBestShift(grey)
        shifted = shift(grey,shiftx,shifty)
        grey = shifted

    cv2.imwrite(image_name, grey)


def prep_input():
    # Iterate over 6 blanks for serial number and date
    for i in range(6):
        preprocess(r'processed_images\s{}.png'.format(i+1))
        preprocess(r'processed_images\d{}.png'.format(i+1))

    # Iterate over 18 unique products, 12 blanks for each product
    for i in range(18):
        for j in range(12):
            preprocess(r'processed_images\{}-{}.png'.format(i+1, j+1))
