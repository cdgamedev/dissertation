import os
from PIL import Image
import numpy as np

# get input of the image count
INPUT_LOCATION = "original-screenshots"
OUTPUT_LOCATION = "output-screenshots"

IMAGE_CROPS = [[1400, 50], [700, 500]]
IMAGE_OUTPUT_WIDTH = 1100

# crop a column out of an image
def image_crop_column(img, crop):
    # get the starting pos
    crop_x = crop[0]
    # get the width of the crop
    crop_width = crop[1]
    
    # convert the image to an array
    img_arr = np.array(img)
    # for the crop area (x axis)
    for x in range(crop_x, img.width):
        # if trying to get data outside of the image, break the cycle
        if (img.width < x + crop_width + 1):
            break
        # for the crop area (y axis)
        for y in range(0, img.height):
            # move the data from the crop_width to the current x value
            img_arr[y, x] = img_arr[y, x + crop_width]
    # convert the array back to an image and return the image
    crop = Image.fromarray(img_arr)
    return crop

# resize the image
def image_resize(img):
    # crop the image to be size [WIDTH, HEIGHT] and return
    resize = img.crop((0, 0, IMAGE_OUTPUT_WIDTH, img.height))
    return resize

# for all files in the directory
for file in os.listdir(INPUT_LOCATION):
    # escape clause if they aren't pngs, continue to next cycle
    if not file.endswith(".png"):
        continue
    # open the image and convert it to greyscale
    img = Image.open(r"{0}\\{1}".format(INPUT_LOCATION, file)).convert('L')
    # crop out the gold icon after the sell price column
    img = image_crop_column(img, IMAGE_CROPS[0])
    # crop out the start bid and quality columns
    img = image_crop_column(img, IMAGE_CROPS[1])
    # resize the image after cropping
    img = image_resize(img)
    # save the image
    img.save(r"{0}\\{1}".format(OUTPUT_LOCATION, file))

print("COMPLETED!")