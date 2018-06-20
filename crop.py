import cv2
import numpy as np
from PIL import Image


def finder(file_name):
    img = cv2.imread('inputs\\'+file_name)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find Harris corners
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
    dst = np.uint8(dst)

    # Find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    # Define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

    a = np.zeros((np.shape(corners)[0], np.shape(corners)[1]+1))
    for i in range(len(corners)):
        a[:,:-1] = corners
        a[i][2] = (corners[i][0] + corners[i][1])

    b = np.sort(a, 0)
    for i in range(len(corners)):
        if (corners[i][0] + corners[i][1] == b[1][2]):
            return (int(corners[i][0])+3, int(corners[i][1])+3)


def crop_invoice(startx, starty, file_name):

    im = Image.open('inputs\\'+file_name)

    # Crop serial values
    x = startx + 2*87
    y = starty
    for i in range(6):
        out = im.crop((x, y, x+75, y+70))
        out.save(r'processed_images\s{}.png'.format(i+1))
        x += 87

    # Crop date values
    x = startx + 2*87
    y = starty + 83
    for i in range(6):
        out = im.crop((x, y, x+75, y+70))
        out.save(r'processed_images\d{}.png'.format(i+1))
        x += 87

    for k in range(18):
        x = startx + 8*87
        y = starty + (4+k)*83
        if k > 8:
            y += 1
        if k > 13:
            y += 2
        for i in range(4):
            out = im.crop((x, y, x+74, y+69))
            out.save(r'processed_images\{}-{}.png'.format(k+1, i+1))
            x += 87
        out = im.crop((x, y, x+74, y+69))
        out.save(r'processed_images\{}-5.png'.format(k+1))
        x += 2*88
        for i in range(6, 10):
            out = im.crop((x, y, x+74, y+69))
            out.save(r'processed_images\{}-{}.png'.format(k+1, i))
            x += 88
        out = im.crop((x, y, x+74, y+69))
        out.save(r'processed_images\{}-10.png'.format(k+1))
        x += 2*88
        out = im.crop((x, y, x+74, y+69))
        out.save(r'processed_images\{}-11.png'.format(k+1))
        x += 88
        out = im.crop((x, y, x+74, y+69))
        out.save(r'processed_images\{}-12.png'.format(k+1))
