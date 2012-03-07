import pyscreenshot as ImageGrab
import cv2.cv as cv

def find_match(file_name, template_array, roi, minimal, debug):

  if not file_name:
    file_name = 'img.png'
    if roi:
      im = ImageGrab.grab(roi)
    else:
      im = ImageGrab.grab()
    im.save(file_name)

  for id, template in enumerate(template_array):
    img = cv.LoadImage(file_name, cv.CV_LOAD_IMAGE_COLOR)
    tpl = cv.LoadImage(template, cv.CV_LOAD_IMAGE_COLOR)
  
    res = cv.CreateImage((img.width - tpl.width + 1, img.height - tpl.height + 1), cv.IPL_DEPTH_32F, 1)
    cv.MatchTemplate(img, tpl, res, cv.CV_TM_SQDIFF)
    (minval, maxval, minloc, maxloc) = cv.MinMaxLoc(res)

    if debug:
      print "minval:" + str(minval)
      print "maxval:" + str(maxval)
      print '"' + template + '": ' + str(minloc)
      print ""

      cv.Rectangle(img, 
        (minloc[0], minloc[1]),
        (minloc[0] + tpl.width, minloc[1] + tpl.height),
      cv.Scalar(0, 1, 0, 0))
      
      cv.NamedWindow('image', cv.CV_WINDOW_AUTOSIZE)
      cv.NamedWindow('template', cv.CV_WINDOW_AUTOSIZE)
      cv.ShowImage('image', img)
      cv.ShowImage('template', tpl)
      
      cv.WaitKey(0)

      cv.DestroyWindow('image')
      cv.DestroyWindow('template')
    
    if minval < minimal:
      return [minloc[0], minloc[1]]
