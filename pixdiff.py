from PIL import Image
import numpy as np

def main(): 
    # load the two images
    image1 = Image.open('image1.png').convert('RGBA')
    image2 = Image.open('image2.png').convert('RGBA')

    # ensure both images are the same size
    if image1.size != image2.size:
        raise ValueError("Images must be the same size for comparison.")

    # convert images to NumPy arrays
    array1 = np.array(image1)
    array2 = np.array(image2)

    # compare the two arrays
    differences = np.where(array1[:, :, :3] != array2[:, :, :3])  # compare RGB channels only

    # create a mask image with the same size as the original images
    mask = Image.new('RGBA', image1.size, (0, 0, 0, 0))  # transparent background

    red_color = (255, 0, 0, 128)  # red with 50% transparency

    # set the pixels in the mask to red where differences are found
    for y, x in zip(differences[0], differences[1]):
        mask.putpixel((x, y), red_color)

    # overlay the mask on the original image
    result = Image.alpha_composite(image1, mask)

    # save or show the result
    result.save('diff.png') 
