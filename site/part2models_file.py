#coding=UTF-8

import cv
import time
import sys

#import pdb
#import json
#from functools import partial
#from flask import Flask, jsonify, request
#from werkzeug.exceptions import default_exceptions, HTTPException
#from werkzeug.datastructures import Headers
#import shutil
#import os, logging, sys, re, time, random
#import subprocess
#import Image
#import ImageChops
#from functions import *
#
#import time, math, random, pdb
#from seed_vin import *
#from config import *
#import Image

def pairs(lst):
    i = iter(lst)
    first = prev = item = i.next()
    for item in i:
        yield prev, item
        prev = item
    yield item, first

def find_match(file_name, template_array, roi, minimal, debug):
  print 'start: ' + str(time.time())

  acummulator = []
  img = cv.LoadImage(file_name, cv.CV_LOAD_IMAGE_COLOR)

  # y - 352 - начальная позиция перед серой полоской первого элемента
  # y - 672 - непосредственно сразу после серой полоской последнего элемента
  # 32 - шаг
  for block in range(352, 672, 32):
    for line in range(2):
      if(line == 0):
        skip_y = 2
      elif(line == 1):
        skip_y = 18

      for element, first in pairs((('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z'), ('(', 'Open Bracket'), (')', 'Close Bracket'), (',', 'Comma'), ('#', 'Octothorpe'), ('-', 'Hyphen'), ('/', 'Slash'), ('.', 'Point'))):

        # Вторые координаты задаются как относительные
        # block+1 (пропускаем красный пунктир)
        # строго высота шрифта - 11
        # 991 - не доходим до пунктира справа
        cv.SetImageROI(img, (20, block+skip_y, 991, 12))

        tpl = cv.LoadImage('images/Toyota EPC/Fonts/Main Font/' + str(element[1]) + '.png', cv.CV_LOAD_IMAGE_COLOR)
        res = cv.CreateImage((cv.GetImageROI(img)[2] - tpl.width + 1, cv.GetImageROI(img)[3] - tpl.height + 1), cv.IPL_DEPTH_32F, 1)
        cv.MatchTemplate(img, tpl, res, cv.CV_TM_SQDIFF)

        for y in range(0, res.height):
          for x in range(0, res.width):
            #print x, y
            s = cv.Get2D(res, y, x)
            if s[0] <= 10:
              #print element[0]
              acummulator.append({'x': x, 'y': y+block+skip_y, 'letter': element[0]})
              #print x, y 
              #if debug:
              #cv.Rectangle(img,
              #    (x, y+block),
              #    (x+tpl.width-1, y+tpl.height-1),
              #cv.Scalar(255, 255, 255, 255), cv.CV_FILLED)

              #cv.ResetImageROI(img)

              #cv.NamedWindow('image', cv.CV_WINDOW_AUTOSIZE)
              ##cv.NamedWindow('template', cv.CV_WINDOW_AUTOSIZE)
              #cv.ShowImage('image', img)
              ##cv.ShowImage('template', tpl)
            x = x + tpl.width
          y = y + tpl.width

  #print time.time()
  #cv.DestroyWindow('template')

  #for f, s in pairs(acummulator):
  #  print s['letter'],

  #cv.ResetImageROI(img)

  #cv.NamedWindow('image', cv.CV_WINDOW_AUTOSIZE)
  ##cv.NamedWindow('template', cv.CV_WINDOW_AUTOSIZE)
  #cv.ShowImage('image', img)
  ##cv.ShowImage('template', tpl)
  #
  #cv.WaitKey(0)

  #cv.DestroyWindow('image')

  #pdb.set_trace()

  acummulator = sorted(sorted(acummulator, key=lambda k: k['x']), key=lambda k: k['y'])
  #accumulator = sorted(acummulator, key=lambda k: k['x']) 
  for i, letter in enumerate(acummulator):
    if((letter['x'] - acummulator[i-1]['x']) > 10):
      sys.stdout.write('\t')
    if((letter['x'] - acummulator[i-1]['x']) < 0):
      print ''
    sys.stdout.write(letter['letter'])
  print '' 
  print '' 
  print 'end ' + str(time.time())


coords = find_match('images/Toyota EPC/Screenshots/Part Number Application to Models/6_.PNG', ['images/Toyota EPC/Screenshots/0.png'], None, 10, True)


