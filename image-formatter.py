import os
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np

# input and output of the images
INPUT_LOCATION = "original-screenshots"
OUTPUT_LOCATION = "output-screenshots"

# the crop locations for the images (x pos, width)
IMAGE_CROPS = [(1405, 25), (700, 500), (222, 210), (0, 130)]
# output width of the images (retain original height)
IMAGE_OUTPUT_WIDTH = 800

# crop a column out of an image
def image_crop_column(img, crop):
    # get the starting pos
    crop_x, crop_width = crop
    
    # convert the image to an array
    img_arr = np.array(img)
    # move the data from the crop_width to the current x value
    img_arr[:, crop_x:img.width-crop_width] = img_arr[:, crop_x+crop_width:img.width]
    # convert the array back to an image and return the image
    crop = Image.fromarray(img_arr)
    return crop

# resize the image
def image_resize(img):
    # crop the image to be size [WIDTH, HEIGHT] and return
    resize = img.crop((0, 0, IMAGE_OUTPUT_WIDTH, img.height))
    return resize

def apply_effect(img):    
    enhancer = ImageEnhance.Brightness(img)
    output = enhancer.enhance(1)
    
    enhancer = ImageEnhance.Contrast(output)
    output = enhancer.enhance(0.8)
    
    output = ImageOps.posterize(output, 1)
    
    output = output.filter(ImageFilter.EDGE_ENHANCE_MORE)
    
    enhancer = ImageEnhance.Sharpness(output)
    output = enhancer.enhance(1)
    
    output = ImageOps.invert(output)
    
    return output

# for all files in the directory
for file in os.listdir(INPUT_LOCATION):
    # escape clause if they aren't pngs, continue to next cycle
    if not file.endswith(".png"):
        continue
    # open the image and convert it to greyscale
    img = Image.open(r"{0}\\{1}".format(INPUT_LOCATION, file)).convert('L')
    # crop out the columns specified
    for i in IMAGE_CROPS:
        img = image_crop_column(img, i)
    # resize the image after cropping
    img = image_resize(img)
    # apply the desired effects to the image
    img = apply_effect(img)
    # save the image
    img.save(r"{0}\\{1}".format(OUTPUT_LOCATION, file))
    print(file)

print("\n\n!! COMPLETED !!")