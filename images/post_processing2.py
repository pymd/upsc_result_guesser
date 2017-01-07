#!/usr/bin/python

# [PoC] tesseract OCR script - tuned for scr.im captcha
#
# Chris John Riley
# blog.c22.cc
# contact [AT] c22 [DOT] cc
# 12/10/2010
# Version: 1.0
#
# Changelog
# 0.1> Initial version taken from Andreas Riancho's \
#      example script (bonsai-sec.com)
# 1.0> Altered to use Python-tesseract, tuned image \
#      manipulation for scr.im specific captchas
#

from PIL import Image

import sys
import subprocess

img = Image.open(sys.argv[1])
img = img.convert("RGBA")

pixdata = img.load()

print type(pixdata)
print "image size:",img.size[0], img.size[1]
print 'pix[23,1]:',pixdata[1,23]
print 'pix[24,1]:',pixdata[1,24]
print 'pix[24,2]:',pixdata[2,24]
print 'pix[25,2]:',pixdata[2,25]
print ''
print 'pix[1,27]:',pixdata[27,1]
print ''
print 'pix[21,17]:',pixdata[17,21]
print 'pix[24,18]:',pixdata[18,24]

# Make the letters bolder for easier recognition

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if (pixdata[x,y][0] < 70) and (pixdata[x,y][1] < 150) and (pixdata[x, y][2] < 70):# and (pixdata[x, y][1] < 20) and (pixdata[x, y][2] < 20):
            pixdata[x,y] = (255,255,255,255)

# Restore some points
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if (pixdata[x,y][0] == 255) and (pixdata[x,y][1] == 255) and (pixdata[x, y][2] == 255):
            count = 0
            try:
                if (pixdata[x-10,y-10][0] < 200) and  (pixdata[x-10,y-10][1] < 200) and (pixdata[x-10,y-10][2] < 200):
                    count+=1
                    if (pixdata[x-10,y][0] < 200) and  (pixdata[x-10,y][1] < 200) and (pixdata[x-10,y][2] < 200):
                        count+=1
                if (pixdata[x+10,y-10][0] < 200) and  (pixdata[x+10,y-10][1] < 200) and (pixdata[x+10,y-10][2] < 200):
                    count+=1
                    if (pixdata[x,y-10][0] < 200) and  (pixdata[x,y-10][1] < 200) and (pixdata[x,y-10][2] < 200):
                        count+=1
                if (pixdata[x-10,y+10][0] < 200) and  (pixdata[x-10,y+10][1] < 200) and (pixdata[x-10,y+10][2] < 200):
                    count+=1
                    if (pixdata[x,y+10][0] < 200) and  (pixdata[x,y+10][1] < 200) and (pixdata[x,y+10][2] < 200):
                        count+=1
                if (pixdata[x+10,y+10][0] < 200) and  (pixdata[x+10,y+10][1] < 200) and (pixdata[x+10,y+10][2] < 200):
                    count+=1
                    if (pixdata[x+10,y][0] < 200) and  (pixdata[x+10,y][1] < 200) and (pixdata[x+10,y][2] < 200):
                        count+=1
                if count >= 4:
                    pixdata[x,y] = (0,0,0,255)
            except:
                continue

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][0] < 90:
            pixdata[x, y] = (0, 0, 0, 255)

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][1] < 136:
            pixdata[x, y] = (0, 0, 0, 255)

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][2] > 0:
            pixdata[x, y] = (255, 255, 255, 255)

img.save("removed_plus.tif")

"""
#   Make the image bigger (needed for OCR)
im_orig = Image.open('input-black.gif')
big = im_orig.resize((1000, 500), Image.NEAREST)
big.save("input-NEAREST.tif")

#   Perform OCR using tesseract-ocr library
from pytesseract import image_to_string
image = Image.open('input-NEAREST.tif')
from pytesseract import image_to_string
image = Image.open('removed_plus.gif')
print image_to_string(image)
"""



p = subprocess.Popen(["tesseract", 'removed_plus.tif', "text_captcha","nobatch","alphanum"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p.wait()
f = open("text_captcha.txt", "r")
#Clean any whitespace characters
captchaResponse = f.read().replace(" ", "").replace("\n", "")
f.close()
print captchaResponse

