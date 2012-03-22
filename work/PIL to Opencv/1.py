import cv
import pyscreenshot as ImageGrab

pil_img = ImageGrab.grab()

cv_img = cv.CreateImageHeader(pil_img.size, cv.IPL_DEPTH_8U, 3)  # RGB image
#cv.SetData(cv_img, pil_img.tostring(), pil_img.size[0]*3)
cv.SetData(cv_img, pil_img.tostring(), pil_img.size[0]*3)
cv.CvtColor(cv_img, cv_img, cv.CV_RGB2BGR)

cv.NamedWindow("pil2ipl")
cv.ShowImage("pil2ipl", cv_img)

cv.WaitKey(0)