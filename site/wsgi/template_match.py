#coding=UTF-8

import sys
import os
import time
import cv

if len(sys.argv) < 4:
  print 'Неправильно указаны параметры, вызов осуществляется так: template_matching.py <изображение> <шаблон> <коэффициент похожести>'
  exit(1)

for file in os.listdir(sys.argv[1]):
  tpl = cv.LoadImage("images/Tecdoc/Shopping Cart 1px.png", cv.CV_LOAD_IMAGE_COLOR)
  img = cv.LoadImage(sys.argv[1] + file, cv.CV_LOAD_IMAGE_COLOR)
  #cv.SetImageROI(img, (1000, 190, 1, 700))
  cv.SetImageROI(img, (1180, 190, 1, 700))
  #threshold = int(sys.argv[3])
  res = cv.CreateImage((1 - tpl.width + 1, 700 - tpl.height + 1), cv.IPL_DEPTH_32F, 1)
  cv.MatchTemplate(img, tpl, res, cv.CV_TM_SQDIFF)
  cv.ResetImageROI(img)
  
  for y in range(0, res.height):
    for x in range(0, res.width):
      s = cv.Get2D(res, y, x)
      if s[0] <= 1000: #threshold:
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
