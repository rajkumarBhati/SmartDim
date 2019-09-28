import numpy as np
import cv2
from helpers.imageHelper  import  Utilities;

class ImageController:

    def readImage(self, coin_diameter=24, unit='cm',
                                 resize_width=700, rotate_angle=0, blur=(5,5), cannyMin=50, cannyMax=100, edge_iterations=1):
        print('reading the image using opencv....');
        imagePath = 'C:/Users/ra014ku/Desktop/Security/sample.jpg';
        #image = cv2.imread('C:/Users/ra014ku/Desktop/Security/python.png')
        # step I.1: load the image, convert it to grayscale, and blur it slightly
        utils = Utilities();
        resized, blurred = utils.optimize_image(imagePath, resize_width, rotate_angle, blur);

        #displayImg(resized, 'resized');
        #displayImg(blurred, 'blurred');

        # step I.2: perform edge detection, then perform a dilation + erotion to close gaps in between object edges
        edge = utils.detect_edge(blurred, cannyMin, cannyMax)

        # step I.3: find and sort objects (sort from left-to-right)
        objs = utils.detect_and_sort_objects(edge)

        # II. LOOP OVER THE OBJECTS IDENTIFIED
        for obj in objs:
            # step II.1: compute the bounding box of the object and draw the box (rectangle)
            box, original_image = utils.create_bounding_box(resized, obj)

            # step II.2: mark the corners of the box
            utils.mark_corners(box, original_image)

            # step II.3: compute the midpoints and mark them
            tltrX, tltrY, blbrX, blbrY, tlblX, tlblY, trbrX, trbrY = utils.get_midpoints(box, original_image)

            # step II.4: compute the Euclidean distance between the midpoints
            dA, dB = utils.get_distances(tltrX, tltrY, blbrX, blbrY, tlblX, tlblY, trbrX, trbrY)

            # step II.5: perform the calibration pixel to millimeters if the pixels per metric has not been initialized
            pixelsPerMetric = dB / coin_diameter

            # step II.6: compute the dimension of the object and show them on the image
            utils.get_dimensions(dA, dB, pixelsPerMetric, original_image, unit, tltrX, tltrY, trbrX, trbrY)

            cv2.imshow(imagePath, original_image)
            cv2.waitKey(0)

def displayImg(img, ImgName):
    # will show the image in a window
    cv2.imshow(ImgName, img);
    cv2.waitKey(0)  # waits until a key is pressed
    cv2.destroyAllWindows()  # destroys the window showing image
