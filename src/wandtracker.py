#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import traceback
import threading
import cv2

class Tracker(threading.Thread):
    
    def __init__(self, cam, caster):
        threading.Thread.__init__(self)
        self.stopped = threading.Event()
        self.caster = caster
        self.cam = cam
        self.__find()
        self.lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
    def __find(self):
        try:
            self.lastFrame = self.cam.processImage(self.cam.getImage())
            
            #TODO: trained image recognition
            self.initialPoints = self.__findWhiteCircles(self.lastFrame)
            if self.initialPoints is not None:
                self.initialPoints.shape = (self.initialPoints.shape[1], 1, self.initialPoints.shape[2])
                self.initialPoints = self.initialPoints[:,:,0:2]
                self.caster.reset()
            print("finding...")
        except:
            e = sys.exc_info()[1]
            print("Error: %s" % e) 
            exit

    def run(self):  
        while not self.stopped.wait(3):  
            self.__find()

    def trackAndWait(self):
        while True:
            try:
                cleanFrame = self.cam.getImage()
                thisFrame = self.cam.processImage(cleanFrame)

                if self.initialPoints is not None:
                    # calculate optical flow
                    p1, st, err = cv2.calcOpticalFlowPyrLK(self.lastFrame, thisFrame, self.initialPoints, None, **self.lk_params)

                    # Select good points
                    if(p1 is not None):
                        good_new = p1[st==1]
                        good_old = self.initialPoints[st==1]

                        # draw the tracks
                        for i,(new,old) in enumerate(zip(good_new,good_old)):
                            a,b = new.ravel()
                            c,d = old.ravel()
                            pt1 = (int(a),int(b))
                            pt2 = (int(c),int(d))
                            
                            # only try to detect gesture on highly-rated points (below 10)
                            if (i<10 and not self.caster.casting):
                                spell = self.caster.detect(a,b,c,d,i)
                                if not spell is None:
                                    self.caster.cast(spell)

                            #dist = math.hypot(a - c, b - d)
                            cleanFrame = cv2.circle(cleanFrame,pt1,5,(0,0,255),-1)
                            #if (dist<120):
                                #cleanFrame = cv2.line(cleanFrame, pt1, pt1, (0,255,0), 2)
                            cleanFrame = cv2.putText(cleanFrame, str(i) + " " + str(spell), pt1, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255)) 
                    # Now update the previous frame and previous points
                    self.lastFrame = thisFrame.copy()
                    self.initialPoints = good_new.reshape(-1,1,2)
                cv2.imshow("Raspberry Potter", cleanFrame)
                #self.cam.show(cleanFrame,12)
            except IndexError:
                print("Index error - Tracking")  
            except:
                e = sys.exc_info()[0]
                print(traceback.format_exc()) 
                print("Tracking Error: %s" % e)
            key = cv2.waitKey(1)
            if key in [27, ord('Q'), ord('q')]: # exit on ESC or q
                break
                
    def __findWhiteCircles(self,image):
        return cv2.HoughCircles(image,cv2.HOUGH_GRADIENT,3,50,param1=240,param2=8,minRadius=2,maxRadius=25)

