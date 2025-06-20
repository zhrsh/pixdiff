#!/usr/bin/env python3

"""
This script is open source under the MIT License. See LICENSE for more info.

Copyright (c) 2025 Zahra A. S.
Email: 182934048+zhrsh@users.noreply.github.com

pixdiff.py

A simple python script to identify pixel-by-pixel differences between two images. 
Only tested for pixel art.

It uses Pillow (PIL) to interperet images into objects and into NumPy arrays for 
better performance. The RGBA value of each pixel of the two arrays is compared. 
The differences are then stored into another NumPy array. The result of the diff 
is configurable, with the default setting generating an output file that overlays 
a color mask on the first image, highlighting the pixels where differences are found.

Currently, you are only able to run this script using the names of the images 
(if in the same directory) or the relative path to the images, not an absolute path. 
The visual output will always be a PNG file, regardless of your input file.

See 'pixdiff --help' for more info.
"""

import argparse
import csv
import os
import sys

from PIL import Image, ImageColor, ImageDraw, UnidentifiedImageError
import numpy as np



NAME = "pixdiff"
VERSION = "0.4.3"



def main():
    """
    Main function. Self explanatory
    Args: none
    Returns: none
    """
    args = run_argparse()

    # assign arguments as variables
    image1_path = args.image1
    image2_path = args.image2

    # =====================================
    #   create rgba color
    # =====================================

    # initialize rgba variable to default value
    rgba = (255, 0, 0, 128)

    # check if --color is provided
    if args.color:
        # parse the list first. should be [str] or [str, int]
        # if only 1 arg provided. should be the str of the color name
        if len(args.color) == 1:
            try:
                rgba = ImageColor.getcolor(args.color[0], 'RGB')
                rgba += (128,) # append default alpha value
            except ValueError:
                printf(f"error: '{args.color[0]}' is not a valid CSS color name.")
                sys.exit(1)
        # if 2 args provided. should be [str, int] with 0 <= int <= 255
        elif len(args.color) == 2:
            # convert 2nd arg to int first
            try:
                custom_alpha = int(args.color[1])
                if 0 <= custom_alpha <= 255:
                    try:
                        rgba = ImageColor.getcolor(args.color[0], 'RGB')
                        rgba += (custom_alpha,) # append custom alpha value
                    except ValueError:
                        printf(f"error: '{args.color[0]}' is not a valid CSS color name.")
                        sys.exit(1)
                else:
                    printf(f"error: '{args.color[1]}' must be an integer between 0 and 255.")
                    sys.exit(1)
            except ValueError:
                printf(f"error: '{args.color[1]}' must be an integer between 0 and 255.")
                sys.exit(1)
        else:
            printf("error: --color can only accept 1 to 2 arguments.")
            sys.exit(1)

    # check if --rgba is provided
    if args.rgba:
        rgba = tuple(args.rgba)  # convert to tuple

    # =====================================
    #   create output path
    # =====================================

    # output path is where the diff will be saved + file name
    # note: extensions will be added later on in the save functions (forces csv and png output)
    if args.path:
        # custom path/name for output file
        output_path = args.path
    else:
        # if user doesn't specify the --path arg, use default
        path_no_ext = os.path.splitext(image1_path)[0] # remove the file extension for image1
        output_path = f"{path_no_ext}_diff"

    # =====================================
    #   comparisson of image1 and image2
    # =====================================

    # results in image1 Image obj, mask Image obj, and diff_coords np array
    #   image1 is the original image1 as an Image obj
    #   mask is an Image obj that colors the pixels that are different in image1 and image2
    #   diff_coords is an np array for csv output
    image1, mask, diff_coords = compare(image1_path, image2_path, rgba)

    # =====================================
    #   saving the output file (image)
    # =====================================

    # save the diff image
    if args.save_none:
        # save nothing if the --no_save flag was included
        # (perhaps they just want to know the coordinates)
        printf("no diff image file saved")
    else:
        # default save (image1 overlayed with the diff mask)
        save_img(image1, mask, output_path, mask_only=args.save_mask) # args.save_mask is a boolean

    # =====================================
    #   saving the output file (csv)
    # =====================================

    # save csv file of the coordinates if --csv_save flag was included
    if args.save_csv:
        save_csv(diff_coords, output_path)



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
        description='A simple script to identify pixel-by-pixel differences between two images. This script is under the MIT License. Copyright (c) 2025 Zahra A. S.',
        epilog='For more information, see documentation at github.com/zhrsh/pixdiff',
        prog=NAME
    )

    # =====================================
    #   initializing groups
    # =====================================

    save_opts = parser.add_argument_group(
        'save options', 
        'options for exporting files.'
    )
    processing_opts = parser.add_argument_group(
        'processing options', 
        'options for processing output files.'
    )

    # =====================================
    #   positional mandatory
    # =====================================

    parser.add_argument(
        'image1', type=str,
        metavar="<IMAGE1>",
        help="the first image to compare and create a diff of."
    )

    parser.add_argument(
        'image2', type=str,
        metavar="<IMAGE2>",
        help="the second image to compare with the first image."
    )

    # =====================================
    #   misc
    # =====================================

    parser.add_argument(
        '-v', '--version', 
        action='version',
        version=f'%(prog)s {VERSION}',
        help='show the program version.'
    )

    # =====================================
    #   boolean flags
    # =====================================

    # save options

    save_opts.add_argument(
        '--save-mask',
        action='store_true', # this will store True if the mask flag is present
        help='save the diff mask with no original image under it.'
    )

    save_opts.add_argument(
        '--save-none',
        action='store_true',
        help='don\'t save or output the diff image file. will cause pixdiff to not generate anything unless specified by another flag.'
    )

    save_opts.add_argument(
        '--save-csv',
        action='store_true',
        help='save every changed pixel by x, y coordinates to a csv file. the csv file is not affected by --save-none.'
    )

    # =====================================
    #   optional arguments
    # =====================================

    save_opts.add_argument('--path', type=str,
        metavar="<FILE_PATH>",
        help='specify the name and relative path of the output file, whether an image or csv. file extension should not be specified (default: image1_path + "_diff")'
    )

    processing_opts.add_argument('--rgba', type=int,
        choices=range(0, 256), # range(start, stop) so, list = 0 =< range < 256
        nargs=4,
        metavar=("<R>", "<G>", "<B>", "<A>"),
        help='4 integer values from 0 to 255 that determines the diff mask color and opacity (default: 255 0 0 128)'
    )

    processing_opts.add_argument('--color', type=str,
        nargs="+",
        metavar=("<COLOR_STRING>", "ALPHA"),
        help='alternative to --rgba that lets you use CSS color name strings from pillow. optionally, provide an alpha value (0-255), if not, the default alpha value of 128 will be used. ignored if --rgba is present.'
    )

    # return parsed args
    return parser.parse_args()



def strip_path(path, include_extension=False, include_path=False):
    """
    Strip the given full path to the base file name, strip the extension only, or both. 
    Can include file extension, can exclude file extension.

    Args: path (full path to image as strings), include_extension (optional, defaults to True)
    Returns: 
        if include_extension is False
            file_name 
            (a string of the base file name WITH extension. e.g. 'img.png')
        if include_extension is False
            file_name_no_ext, extension 
            (a string of the base file name WITHOUT extension. e.g. 'img' and its extension)
    """
    if include_path is False:
        # get base file name without path
        path = os.path.basename(path)

    if include_extension is False:
        # strip file extension if include_extension is false:
        file_name_no_ext, extension = os.path.splitext(path)
        return file_name_no_ext, extension
    else:
        # file name with extension
        return path



def load_image(image_path):
    """
    Load an image from the specified path as a PIL object.

    Args: image_path (path to image as a string)
    Returns: image (PIL Image object)
    """
    if not os.path.exists(image_path):
        printf(f"error: image not found: {image_path}")
        sys.exit(1)

    try:
        return Image.open(image_path).convert('RGBA')
    except FileNotFoundError:
        printf(f"error: file not found: {image_path}")
        sys.exit(1)
    except UnidentifiedImageError:
        printf(f"error: the file at {image_path} is not a valid image.")
        sys.exit(1)
    except Image.DecompressionBombError:
        printf(f"error: the image at {image_path} is too large and may be a decompression bomb.")
        sys.exit(1)
    except IOError as e:
        printf(f"error: an I/O error occurred while loading {image_path}:\n{e}")
        sys.exit(1)
    except Exception as e:
        printf(f"error: an unexpected error occurred:\n{e}")
        raise  # re-raise the exception to allow it to propagate



def compare_validator(image1, image2, max_resolution=1024):
    """
    Image comparisson validator. Makes sure that two images are ready and valid for comparisson.

    Args: 
        image1 (Image obj): First image to compare.
        image2 (Image obj): Second image to compare.
        max_resolution (int): Maximum total number of pixels allowed for comparison.

    Returns: 
        bool: True if images are valid, False if images are not valid for comparison.
    """
    # check if images are the same format
    if image1.format != image2.format:
        printf("error: images must be the same format for comparison.")
        return False

    # check if images are the same in resolution (width, height)
    elif image1.size != image2.size:
        printf("error: images must be the same size for comparison.")
        return False

    # check if image are too large in resolution (total must be less than max_resolution)
    elif image1.size[0] + image1.size[1] > max_resolution:
        printf("error: the images are too large in resolution for comparison.")
        return False
        # no need to check image2 because they have the same resolution

    else:
        return True



def compare(image1_path, image2_path, rgba=(255, 0, 0, 128)):
    """
    Compare two images pixel by pixel. 
    Each pixel diff is detected comparing the RGBA value of each pixel.

    Args: image1_path, image2_path (paths to images as strings), rgba (tuple, the color of the diff mask)
    Returns: image1 (Image obj), mask (Image obj), differences (np array with x,y diff coordinates)
    """
    # load the two images as PIL objects
    image1 = load_image(image1_path)
    image2 = load_image(image2_path)

    # check if images are valid for comparisson, returns False if images are not valid
    if compare_validator(image1, image2) is False:
        sys.exit(1)

    # convert images to NumPy arrays
    array1 = np.array(image1)
    array2 = np.array(image2)

    # compare the two arrays including the alpha channel
    differences = np.where(array1 != array2)  # compare all channels (RGBA)
    # get the coords and put them in a list of unique tuple pairs (x, y)
    diff_coords = list(set(zip(differences[1], differences[0])))

    # create a mask image with the same size as the original images
    mask = Image.new('RGBA', image1.size, (0, 0, 0, 0))  # transparent background

    # create draw object to draw on empty mask
    draw_mask = ImageDraw.Draw(mask)
    # set the pixels in the mask to red where differences are found
    draw_mask.point(diff_coords, rgba) # default rgba is red with 50% transparency

    printf(f"differing pixels found: {len(diff_coords)}")

    return image1, mask, diff_coords



def save_img(image1, mask, output_path, mask_only=False):
    """
    Saves either the original image1 overlayed with the diff mask or only the 
    diff mask itself to the current directory or specified directory
    
    Args: 
        image1_path (str)
        image1 (Image obj)
        mask (Image obj), 
        output_path (str): where the output file will be written. No extension in order to force to .png
        mask_only (optional, defeaults to False)
    Returns: none
    """
    png_file_path = f"{output_path}.png"

    if mask_only is True:
        # result: the mask alone
        result = mask
    else:
        # result: an overlay of the mask on the original image
        result = Image.alpha_composite(image1, mask)

    try:
        # printf info and save
        result.save(png_file_path, 'PNG')
        printf(f"successfully saved visual differences to {png_file_path}")
    except FileNotFoundError:
        printf(f"error: the file path '{png_file_path}' does not exist.")
    except IOError as e:
        printf(f"error: an I/O error occurred while saving the image:\n{e}")
    except ValueError as e:
        printf(f"error: an invalid value occurred while saving the image:\n{e}")
    except Image.DecompressionBombError:
        printf("error: the image is too large and may be a decompression bomb.")
    except Exception as e:
        printf(f"error: an unexpected error occurred:\n{e}")
        raise  # re-raise the exception to allow it to propagate



def save_csv(differences, output_path):
    """
    Write the differences coordinates to a CSV file.
    Args:
        differences (tuple): tuple containing two arrays (y-coordinates, x-coordinates).
        output_path (str): path to the CSV file where differences will be saved (write). No extension in order to force to .csv
    Returns: none
    """

    csv_file_path = f"{output_path}.csv"

    try:
        # write the differences to a CSV file
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['x', 'y'])     # header
            writer.writerows(differences)   # write the coordinates
        printf(f"successfully saved differences to {csv_file_path}")

    except FileNotFoundError:
        printf(f"error: the file path '{csv_file_path}' does not exist.")
    except IOError as e:
        printf(f"error: error writing to file {csv_file_path}:\n{e}")
    except Exception as e:
        printf(f"error: an unexpected error occurred:\n{e}")
        raise  # re-raise the exception to allow it to propagate

if __name__ == "__main__":
    main()