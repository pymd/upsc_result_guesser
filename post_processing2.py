from PIL import Image

#import sys
import subprocess

def do_processing(image_name, output_name):

    #img = Image.open(sys.argv[1])
    img = Image.open(image_name)
    img = img.convert("RGBA")

    pixdata = img.load()


    # Remove plus signs
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if (pixdata[x,y][0] < 70) and (pixdata[x,y][1] < 150) and (pixdata[x, y][2] < 70):
                pixdata[x,y] = (255,255,255,255)

    # Restore lost points
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

    # Make the letters bolder for easier recognition
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

    img.save(output_name)