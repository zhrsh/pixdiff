# pixdiff.py

A simple script to identify pixel-by-pixel differences between two images. Recommended for pixel art.

It uses Pillow (PIL) to interperet images into objects and into NumPy arrays for better performance. The RGBA value of each pixel of the two array is compared. The differences are then stored into another NumPy array. The result of the diff is configurable, with the default setting generating an output file that overlays a color mask on the first image, highlighting the pixels where differences are found.

Currently, you are only able to run this script using the names of the images (if in the same directory) or the relative path to the images, not an absolute path. The visual output will always be a PNG file, regardless of your input file.

## Basic usage

The most basic way to use this script is to run it without any flags:

```bash
pixdiff relative/path/to/first_image.png relative/path/to/second_image.png
```

This will output `first_image_diff.png` in the same directory as where the first image is, so `relative/path/to/first_image_diff.png`.

## Example usage

All these examples can be run using [`example_batch.sh`](example_batch.sh)

Say I have `example1.png` and `example2.png`:

<p float="left">
  <img src="readme_images/example1.png" width="256" style="margin-right: 16px;">
  <img src="readme_images/example2.png" width="256">
</p>

If I run the default usage:

```bash
pixdiff example1.png example2.png
```

The script will output `example1_diff.png`, which is `example1.png` overlayed by the differences found in `example2.png` (the highlights on the leaves and trunk):

<p float="left">
  <img src="readme_images/example_default.png" width="256">
</p>

Below are the commands and optional flags you can use, which can also be viewed using `--help` or `-h` command.

```plaintext
optional arguments:

    -h, --help
        show this help message and exit

    --version, -v 
        show the program version.

    --save-mask    
        save the diff mask with no original image under it.

    --save-none    
        don't save or output the diff image file.
        will cause pixdiff to not generate anything
        unless specified by another flag.

    --save-csv     
        save every changed pixel by x, y coordinates
        to a csv file. is not effected by save-none

    --path <OUTPUT_FILE_PATH>
        specify the name and relative path of the
        output file, whether an image or csv.
        file extension should not be specified
        (default: image1_path + "_diff")

    --alpha <ALPHA_VALUE>
        an integer value from 1 to 255 that
        determines the diff mask opacity/alpha
        value (default: 128)
```

## License

This script, pixdiff.py and example_batch.sh, is licensed under the MIT License. See the [LICENSE](LICENSE) file for more info.

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><span property="dct:title">The example images in this README</span> by <span property="cc:attributionName">Zahra A. S.</span> are licensed under <a href="https://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""></a></p>