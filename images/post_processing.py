from PIL import Image

img = Image.open('input-NEAREST.tif')
img = img.convert("RGBA")

pixdata = img.load()
print type(pixdata)
print 'image size:',img.size[0],img.size[1]

#print pixdata[857,258]

# the last + in the image
r = range(-7,12)
print r
for y in r:
    for x in r:
        print '%3d' % pixdata[858+x, 257+y][0],
    print ''

def identify_plus():
    pass

def print_matrix(m):
    for y in range(len(m)):
        for x in range(len(m[0])):
            try:
                print m[y][x],
            except:
                print 'x,y is:',x,y
                return
        print ''

image_matrix = []
for y in range(img.size[1]):
    inner_matrix = []
    for x in range(img.size[0]):
        inner_matrix.append(pixdata[x,y][0])
    image_matrix.append(inner_matrix)

print len(image_matrix[0])
print len(image_matrix)

#print_matrix(image_matrix)

img.save("output-NEAREST.tif")

# Perform OCR using tesseract-ocr library
from pytesseract import image_to_string
image = Image.open('output-NEAREST.tif')
print image_to_string(image)
