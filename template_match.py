#coding=UTF-8
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages/')
sys.path.append("C:\\opencv\\build\\python\\2.7")

import cv2.cv as cv
#from cv import *
if len(sys.argv) < 4:
  print 'Неправильно указаны параметры, вызов осуществляется так: template_matching.py <изображение> <шаблон> <коэффициент похожести>'
  exit(1)

img = cv.LoadImage(sys.argv[1], cv.CV_LOAD_IMAGE_COLOR)
tpl = cv.LoadImage(sys.argv[2], cv.CV_LOAD_IMAGE_COLOR)
# 292817 (Hyundai Microcat)
threshold = int(sys.argv[3])
res = cv.CreateImage((img.width - tpl.width + 1, img.height - tpl.height + 1), cv.IPL_DEPTH_32F, 1)
cv.MatchTemplate(img, tpl, res, cv.CV_TM_SQDIFF)

for y in range(0, res.height):
  for x in range(0, res.width):
    s = cv.Get2D(res, y, x)
    if s[0] <= threshold:
      cv.Rectangle(img,
          (x-1, y-2),
          (x+tpl.width, y+tpl.height),
          cv.Scalar(0, 1, 0, 0))

cv.NamedWindow("reference", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("template", cv.CV_WINDOW_AUTOSIZE)
cv.ShowImage("reference", img)
cv.ShowImage("template", tpl)

cv.WaitKey(0)
