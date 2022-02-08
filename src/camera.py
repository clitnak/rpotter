#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class Camera:

    def __init__(self, display=True, showWhichState=12):
        self.showWhichState = showWhichState
        self.display = display
        if self.display:
            cv2.namedWindow("Raspberry Potter")
        self.cam = cv2.VideoCapture(cv2.CAP_V4L2);
        self.cam.set(3, 640)
        self.cam.set(4, 480)

        #cam.set(3, 1280)
        #cam.set(4, 720)
        
    def getImage(self):
        image = None;
        while(image is None):
            rval, image = self.cam.read()    
        image = cv2.flip(image,1)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        return image


    def processImage(self, image):
        self.show(image, 1)
        
        (T, image) = cv2.threshold(image, 170, 255, cv2.THRESH_BINARY)
        self.show(image, 2)
        
        dilate_kernel = np.ones((5,5), np.uint8)
        image = cv2.dilate(image, dilate_kernel, iterations=1)
        self.show(image, 3)
        
        (T, image) = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
        self.show(image, 4)
        
        image = cv2.GaussianBlur(image,(15,15),1.5)
        self.show(image, 5)
        
        (T, image) = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)
        self.show(image, 6)
        
        image = cv2.GaussianBlur(image,(15,15),1.5)
        self.show(image, 7)
        
        (T, image) = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)
        self.show(image, 8)
        
        image = cv2.GaussianBlur(image,(11,11),1.5)
        self.show(image, 9)
       
        return image
    
    def show(self, image, whichImage = -1):
        if self.display and (whichImage == -1 or self.showWhichState == whichImage):
            cv2.imshow("Raspberry Potter", image)
            
    def end(self):
        self.cam.release()
        cv2.destroyAllWindows()