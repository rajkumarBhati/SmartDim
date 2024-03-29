
from __future__ import print_function, division
from builtins import input
import imutils
from imutils import contours
from imutils import perspective
import numpy as np
import cv2


class Utilities:
    def __init__(self):
        print('for more details kindly visit Rajkumar Bhati.....')

    def optimize_image(self, filename, resize_width, rotate_angle, blur):
        print('STARTED :: optimize_image() of Utilities')
        image = cv2.imread(filename)
        image = imutils.resize(image, width=resize_width)
        image = imutils.rotate(image, angle=rotate_angle)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, blur, 0)
        print('END :: optimize_image() of Utilities')
        return image, gray

    def detect_edge(self, image, cannyMin, cannyMax):
        print('STARTED :: detect_edge() of Utilities')
        edged = cv2.Canny(image, cannyMin, cannyMax)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        print('END :: detect_edge() of Utilities')
        return edged

    def detect_and_sort_objects(self, image):
        print('STARTED :: detect_and_sort_objects() of Utilities')
        cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cnts = cnts[0]
        (cnts, _) = contours.sort_contours(cnts)
        print('END :: detect_and_sort_objects() of Utilities')
        return cnts

    def create_bounding_box(self, image, target_object, draw=True):
        print('STARTED :: create_bounding_box() of Utilities')
        orig = image.copy()
        box = cv2.minAreaRect(target_object)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype='int')

        '''
        order the points in the object such that they appear in top-left, top-right,
        bottom-right, and bottom-left order, then draw the outline of the rotated
        bounding box
        '''
        box = perspective.order_points(box)
        if draw == True: cv2.drawContours(orig, [box.astype('int')], -1, (0, 255, 0), 1)
        print('END :: create_bounding_box() of Utilities')
        return box, orig

    def mark_corners(self, box, image):
        for (x, y) in box:
            cv2.circle(image, (int(x), int(y)), 3, (0, 0, 255), -1)

    def get_midpoints(self, box, image, draw=True):
        def midpoint(ptA, ptB):
            return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

        # unpack the ordered bounding box
        (tl, tr, br, bl) = box

        # compute the midpoint between the top-left and top-right, followed by the midpoint between bottom-left and bottom-right
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

        # compute the midpoint between the top-left and bottom-left points, followed by the midpoint between the top-right and bottom-right
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        if draw:
            # draw the midpoints on the image
            cv2.circle(image, (int(tltrX), int(tltrY)), 3, (255, 0, 0), -1)
            cv2.circle(image, (int(blbrX), int(blbrY)), 3, (255, 0, 0), -1)
            cv2.circle(image, (int(tlblX), int(tlblY)), 3, (255, 0, 0), -1)
            cv2.circle(image, (int(trbrX), int(trbrY)), 3, (255, 0, 0), -1)

            # draw lines between the midpoints
            cv2.line(image, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 1)
            cv2.line(image, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 1)

        return tltrX, tltrY, blbrX, blbrY, tlblX, tlblY, trbrX, trbrY

    def get_distances(self, tltrX, tltrY, blbrX, blbrY, tlblX, tlblY, trbrX, trbrY):
        from scipy.spatial import distance as dist
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        return dA, dB

    def get_dimensions(self, dA, dB, ratio, image, unit, tltrX, tltrY, trbrX, trbrY):
        dimA = dA / ratio
        dimB = dB / ratio
        # draw the dimensions on the image
        cv2.putText(image, "{:.1f}{}".format(dimA, unit), (int(tltrX - 15), int(tltrY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(image, "{:.1f}{}".format(dimB, unit), (int(trbrX + 10), int(trbrY)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)