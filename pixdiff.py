from PIL import Image
import argparse
import csv
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
    alpha = args.alpha

    image1, mask, diff_coords = compare(image1_path, image2_path, alpha)

    # save the diff image
    if args.save_none:
        # if user added --no_save flag (perhaps they just want to know the coordinates)
        printf("no diff image file saved")
    elif args.save_mask:
        # if user added --mask flag
        save_img(image1_path, image1, mask, mask_only=True)
    else:
        # default save (image1 + diff mask overlay)
        save_img(image1_path, image1, mask, mask_only=False)

    # save csv file of the coordinates if --csv_save is included
    if args.save_csv:
        file_name, _ = strip_path(image1_path, include_extension=False) # default file name
        save_csv(diff_coords, file_name + "_diff.csv")



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

    # =====================================
    #   positional mandatory
    # =====================================

    parser.add_argument(
        'image1',
        type=str, 
        help="the first image to compare and create a diff of."
    )

    parser.add_argument(
        'image2',
        type=str, 
        help="the second image to compare with the first image."
    )

    # =====================================
    #   misc
    # =====================================

    parser.add_argument(
        '--version', '-v', 
        action='version', 
        version=f'%(prog)s {VERSION}', 
        help='show the program version.'
    )

    # =====================================
    #   boolean option flags
    # =====================================

    # save options

    parser.add_argument(
        '--save-mask',
        action='store_true', # this will store True if the mask flag is present
        help='save the diff mask with no original image under it.'
    )

    parser.add_argument(
        '--save-none',
        action='store_true',
        help='don\'t save or output the diff image file. will cause pixdiff to not generate anything unless specified by another flag.'
    )

    parser.add_argument(
        '--save-csv',
        action='store_true',
        help='save every changed pixel by x, y coordinates to a csv file. is not effected by save-none'
    )

    # RGBA options 

    parser.add_argument('--alpha', type=int, 
        choices=range(1, 256), # range(start, stop) so, list = 1 < range < 256
        default=128, # default value
        metavar="INT",
        help='an integer value from 1 to 255 that determines the diff mask opacity/alpha value (default: 128)'
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
        printf(f"error: image not found: {image1_path}")
        sys.exit(1)
    if not os.path.exists(image2_path):
        printf(f"error: image not found: {image2_path}")
        sys.exit(1)

    try:
        # load the images
        image1 = Image.open(image1_path).convert('RGBA')
        image2 = Image.open(image2_path).convert('RGBA')
        
        return image1, image2

    except Exception as e:
        printf(f"an unexpected error occurred: {e}")



def compare(image1_path, image2_path, alpha_value=128):
    """
    Compare two images pixel by pixel. Each pixel diff is detected comparing the RGBA value of each pixel.
    Args: image1_path, image2_path (paths to images as strings)
    Returns: image1 (Image obj), mask (Image obj), differences (np array with x,y diff coordinates)
    """
    # load the two images as PIL objects
    # includes error handling
    image1, image2 = load_images(image1_path, image2_path)

    # check if images are the same dimensions (width, height)
    if image1.size != image2.size:
        printf("error: images must be the same size for comparison.")
        sys.exit(1)

    # check if images are too large in dimension (width, height)
    if image1.size[0] + image2.size[1] > 2048:
        printf(f"error: the images are too large in dimension for comparison.")
        sys.exit(1)
        # no need to do image2 because they have the same dimensions

    # convert images to NumPy arrays
    array1 = np.array(image1)
    array2 = np.array(image2)

    # compare the two arrays including the alpha channel
    differences = np.where(array1 != array2)  # compare all channels (RGBA)

    # create a mask image with the same size as the original images
    mask = Image.new('RGBA', image1.size, (0, 0, 0, 0))  # transparent background

    red_color = (255, 0, 0, alpha_value)  # red with 50% transparency

    # set the pixels in the mask to red where differences are found
    for y, x in zip(differences[0], differences[1]):
        mask.putpixel((x, y), red_color)

    return image1, mask, differences



def save_img(image1_path, image1, mask, mask_only=False):
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
    printf(f"successfully saved visual differences to {file_name}")
    result.save(file_name) 



def save_csv(differences, csv_file_path):
    """
    Write the differences coordinates to a CSV file.
    Args:
        differences (tuple): tuple containing two arrays (y-coordinates, x-coordinates).
        csv_file_path (str): path to the CSV file where differences will be saved.
    """
    
    # get the coordinates of the differences
    diff_coords = list(zip(differences[1], differences[0]))  # (x, y) format

    # remove duplicates while preserving order
    unique_diff_coords = []
    seen = set()
    for coord in diff_coords:
        if coord not in seen:
            seen.add(coord)
            unique_diff_coords.append(coord)

    try:
        # write the differences to a CSV file
        with open(csv_file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['x', 'y'])     # header
            writer.writerows(unique_diff_coords)   # write the coordinates
        printf(f"successfully saved differences to {csv_file_path}")

    except IOError as e:
        printf(f"error writing to file {csv_file_path}: {e}")
    except Exception as e:
        printf(f"an unexpected error occurred: {e}")

if __name__ == "__main__":
    main()