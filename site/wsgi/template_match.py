#coding=UTF-8
import sys
import os
import time
sys.path.append('/usr/local/lib/python2.7/site-packages/')
sys.path.append("C:\\opencv\\build\\python\\2.7")

#import cv2.cv as cv
import cv
#from cv2 import cv2.CvRect 

#path = '/Users/woto/python/EPC/site/wsgi/images/Tecdoc/Screenshots/'
#from cv import *

if len(sys.argv) < 4:
  print 'Неправильно указаны параметры, вызов осуществляется так: template_matching.py <изображение> <шаблон> <коэффициент похожести>'
  exit(1)

tpl = cv.LoadImage(sys.argv[2], cv.CV_LOAD_IMAGE_COLOR)

for file in os.listdir(sys.argv[1]):
  img = cv.LoadImage(sys.argv[1] + file, cv.CV_LOAD_IMAGE_COLOR)
  cv.SetImageROI(img, (1000, 190, 1, 700))
  # 292817 (Hyundai Microcat)
  threshold = int(sys.argv[3])
  res = cv.CreateImage((1 - tpl.width + 1, 700 - tpl.height + 1), cv.IPL_DEPTH_32F, 1)
  cv.MatchTemplate(img, tpl, res, cv.CV_TM_SQDIFF)
  cv.ResetImageROI(img)

  #rois = []
  for y in range(0, res.height):
    for x in range(0, res.width):
      s = cv.Get2D(res, y, x)
      if s[0] <= threshold:
        cv.SetImageROI(img, (x+210, y+190, x+600, tpl.height))
        cv.NamedWindow("reference", cv.CV_WINDOW_AUTOSIZE)
        cv.ShowImage("reference", img)
        cv.WaitKey(0)
        #pass
        #cv.Rectangle(img,
        #    (x+210, y+190),
        #    (x+tpl.width+100+500, y+tpl.height+189),
        #    cv.Scalar(0, 1, 0, 0))
        


  cv.NamedWindow("reference", cv.CV_WINDOW_AUTOSIZE)
  cv.NamedWindow("template", cv.CV_WINDOW_AUTOSIZE)
  cv.ShowImage("reference", img)
  cv.ShowImage("template", tpl)

  cv.WaitKey(0)
