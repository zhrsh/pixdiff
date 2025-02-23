from PIL import Image
import argparse
import numpy as np
import os
import sys

NAME = "pixdiff"
VERSION = "0.1.0"

def main(): 
    args = run_argparse()

    # assign positional arguments as images
    image1_path = args.image1
    image2_path = args.image2

    # compare image1 and image2, assign returns
    image1, mask = compare(image1_path, image2_path)

    # save the diff image
    if args.mask:
        # if user added --mask flag
        save(image1_path, image1, mask, mask_only=True)
    else:
        save(image1_path, image1, mask, mask_only=False)

def printf(string):
    """
    Print messages formatted using the program name. "{NAME}: {string}\\n"
    Args: string (str to print)
    Returns: none
    """
    sys.stdout.write(f"{NAME}: {string}\n")

def run_argparse():
    """
    Parse the user's command line arguments. Runs at the beginning of the program.
    Args: none
    Returns: parser.parse_args() (parsed arguments. an argparse obj)
    """

    parser = argparse.ArgumentParser(
        description='Find differences between two images pixel by pixel. Recommended for pixel art.',
        prog=NAME
    )

    # positional mandatory 1
    parser.add_argument(
        'image1',
        type=str, 
        help="The first image to compare and create a diff of."
    )

    # positional mandatory 2
    parser.add_argument(
        'image2',
        type=str, 
        help="The second image to compare with the first image."
    )

    # misc
    parser.add_argument(
        '--version', '-v', 
        action='version', 
        version=f'%(prog)s {VERSION}', 
        help='Show the program version.'
    )

    # boolean option flags
    parser.add_argument(
        '--mask',
        action='store_true',  # this will store True if the mask flag is present
        help='Only save the "diff mask" with no original image under it. Useful for further analysis and visualization in an image/art software.'
    )

    # return parsed args
    return parser.parse_args()

def strip_path(path, include_extension=True):
    """
    Strip the given full path to the base file name. Can include file extension, can exclude file extension.
    Args: path (full path to image as strings), include_extension (optional, defaults to True)
    Returns: 
        if include_extension is True
            file_name (a string of the base file name WITH extension. e.g. 'img.png')
        if include_extension is False
            file_name_no_ext, extension (a string of the base file name WITHOUT extension. e.g. 'img' and its extension)
    """
    # get base file name
    file_name = os.path.basename(path)

    if include_extension == False:
        # strip file extension if include_extension is false:
        file_name_no_ext, extension = os.path.splitext(file_name)
        return file_name_no_ext, extension
    else:
        # file name with extension
        return file_name

def load_images(image1_path, image2_path):
    """
    Load image1 and image2 from the specified path as PIL objects
    Args: image1_path, image2_path (paths to images as strings)
    Returns: image1, image2 (PIL Image objects)
    """
    # check if the files exist before trying to open them
    if not os.path.exists(image1_path):
        raise FileNotFoundError(f"image not found: {image1_path}")
    if not os.path.exists(image2_path):
        raise FileNotFoundError(f"image not found: {image2_path}")

    try:
        # load the images
        image1 = Image.open(image1_path).convert('RGBA')
        image2 = Image.open(image2_path).convert('RGBA')
        
        return image1, image2

    except Exception as e:
        raise RuntimeError(f"an error occurred while loading images: {e}")

def compare(image1_path, image2_path):
    """
    Compare two images pixel by pixel. Each pixel diff is detected comparing the RGBA value of each pixel.
    Args: image1_path, image2_path (paths to images as strings)
    Returns: none
    """
    # load the two images with error handling
    image1, image2 = load_images(image1_path, image2_path)

    # check if images are the same dimensions (width, height)
    if image1.size != image2.size:
        raise ValueError("images must be the same size for comparison.")

    # check if images are too large in dimension (width, height)
    if image1.size[0] + image1.size[1] == 1024:
        raise ValueError(f"the image {image1} is too large for comparison.")
        # no need to do image2 because they have the same dimensions

    # convert images to NumPy arrays
    array1 = np.array(image1)
    array2 = np.array(image2)

    # compare the two arrays including the alpha channel
    differences = np.where(array1 != array2)  # compare all channels (RGBA)

    # create a mask image with the same size as the original images
    mask = Image.new('RGBA', image1.size, (0, 0, 0, 0))  # transparent background

    red_color = (255, 0, 0, 128)  # red with 50% transparency

    # set the pixels in the mask to red where differences are found
    for y, x in zip(differences[0], differences[1]):
        mask.putpixel((x, y), red_color)

    return image1, mask

def save(image1_path, image1, mask, mask_only=False):
    """
    Saves either the original image1 overlayed with the diff mask or only the diff mask itself to the current directory or specified directory
    Args: image1_path (str), image1 (Image obj), mask (Image obj), mask only (optional, defeaults to False)
    Returns: none
    """
    if mask_only == False:
        # result: an overlay of the mask on the original image
        result = Image.alpha_composite(image1, mask)
    elif mask_only == True:
        # result: the mask alone
        result = mask

    # split the image_name (e.g. 'my_img') and the image_extension (e.g. '.png')
    image_name, image_extension = strip_path(image1_path, include_extension=False)

    # combine variables back into a filename, original file name + _diff + extension
    file_name = f"{image_name}_diff{image_extension}"

    # printf info and save
    printf(f"diff saved as {file_name}")
    result.save(file_name) 


if __name__ == "__main__":
    main()