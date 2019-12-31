import cv2 as cv

MAX_SIZE = 399


class ArUcoDecoder:
    def __init__(self, img):
        self.image = img
        self.image_bw = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        self.id = 0

    def extract_aruco(self):
        ret, thresh_im = cv.threshold(self.image_bw, 127, 255, cv.THRESH_BINARY_INV)
        contours, hierarchy = cv.findContours(thresh_im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = contours[0]
        epsilon = 0.1 * cv.arcLength(contours, True)
        approxCurve = cv.approxPolyDP(contours, epsilon, True)
        self.aruco = self.image_bw[approxCurve[0, 0, 1]:approxCurve[2, 0, 1], approxCurve[0, 0, 0]:approxCurve[2, 0, 0]]

    def extract_id(self):
        self.extract_aruco()
        self.aruco = cv.resize(self.aruco, (MAX_SIZE, MAX_SIZE))
        width = int(MAX_SIZE/7)
        self.aruco = self.aruco[width: width * 6, width: width * 6]
        for y in range(5):
            v1 = self.aruco[int(y * width + width/2), int(width + width/2)]
            v2 = self.aruco[int(y * width + width/2), int(3 * width + width/2)]
            if v1 == 255:
                v1 = 1
            if v2 == 255:
                v2 = 1
            self.id = self.id * 2 + v1
            self.id = self.id * 2 + v2
        return self.id
