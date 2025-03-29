# pixdiff

A simple python script to identify pixel-by-pixel differences between two images. Only tested for pixel art.

It uses [Pillow](https://github.com/python-pillow/Pillow/) (PIL) to interperet images into objects and into [NumPy](https://numpy.org) arrays for better performance. The RGBA value of each pixel of the two arrays is compared. The differences are then stored into another NumPy array. The result of the diff is configurable, with the default setting generating an output file that overlays a color mask on the first image, highlighting the pixels where differences are found.

Currently, you are only able to run this script using the names of the images (if in the same directory) or the relative path to the images, not an absolute path. The visual output will always be a PNG file, regardless of your input file.

## Dependencies

Python 3.9.6 or higher

## Installation

### Linux/MacOS/UNIX-like
Assuming you have ~/bin as a PATH environment variable and python/pip installed, run this in your terminal:
```bash
python3 -m pip install --upgrade Pillow NumPy
git clone https://github.com/zhrsh/pixdiff.git
cd pixdiff
./install.sh
```

You can modify the DIR_USR variable in install.sh if a different installation path is needed.

## Basic Usage

The most basic way to use this script is to run it without any flags:

```bash
pixdiff relative/path/to/first_image.png relative/path/to/second_image.png
```

This will output `first_image_diff.png` in the same directory as where the first image is, so `relative/path/to/first_image_diff.png`.

### Example

All these examples can be run using [`example_batch.sh`](example_batch.sh)

Say I have `example1.png` and `example2.png`:

<p float="left">
  <img src="readme_images/example1.png" width="256">
  <img src="readme_images/example2.png" width="256">
</p>

If I run the default usage:

```bash
pixdiff example1.png example2.png
```

The script will output `example1_diff.png`, which looks like this:

<p float="left">
  <img src="readme_images/example_default.png" width="256">
</p>

This is just `example1.png` overlayed by the differences found in `example2.png` (the highlights on the leaves and trunk). By default, the mask overlay is the color red with an alpha value of 128. This can be modified using optional arguments.

## Optional Arguments

Below are the optional arguments and flags you can use, which can also be viewed using `--help` or `-h` command.

- `-h`, `--help`
    - Show this help message and exit.

- `-v`, `--version`
    - Show the program version.

- [`--save-mask`](#--save-mask)
    - Save the diff mask with no original image under it.

- `--save-none`
    - Don't save or output the diff image file. This will cause `pixdiff` to not generate anything unless specified by another flag.

- [`--save-csv`](#--save-csv)
    - Save every changed pixel by x, y coordinates to a CSV file. The CSV file is not affected by `--save-none`.

- `--path <OUTPUT_FILE_PATH>`
    - Specify the name and relative path of the output file, whether an image or CSV. The file extension should not be specified (default: `image1_path + "_diff"`).

- [`--rgba <R> <G> <B> <A>`](#--rgba)
    - 4 integer values from 0 to 255 that will determine the diff mask color and opacity (default: 255 0 0 128)

- [`--color <COLOR_STRING>`](#--color)
    - An alternative to --rgba that lets you use CSS color name strings from pillow. This flag is ignored if `--rgba` is provided.

---

### `--save-mask`

A flag that, when included, saves the default diff mask without any image under it. Usefeul if you want to work with the diff mask pixels in your art program.

Example:

```bash
pixdiff example1.png example2.png --save-mask
```

<p float="left">
  <img src="readme_images/example1.png" width="128">
  <img src="readme_images/example2.png" width="128">
  <img src="readme_images/arrow.png" height="128">
  <img src="readme_images/example_mask.png" width="128">
</p>

---

### `--rgba`

A optional argument that allows you to control the color and opacity of the diff mask (RGBA values). This option requires four supplementary arguments representing the Red, Green, Blue, and Alpha (opacity) values. Each must be integers with the value from 1 to 255. Without this argument, the default RGBA value is (255, 0, 0, 128).

Example:

```bash
pixdiff example1.png example2.png --rgba 94 48 235 250
```

<p float="left">
  <img src="readme_images/example1.png" width="128">
  <img src="readme_images/example2.png" width="128">
  <img src="readme_images/arrow.png" height="128">
  <img src="readme_images/example_rgba.png" width="128">
</p>

Another example:

Using `--save-mask` and `--rgba` together

```bash
pixdiff example1.png example2.png --save-mask --rgba 94 48 235 250
```

<p float="left">
  <img src="readme_images/example1.png" width="128">
  <img src="readme_images/example2.png" width="128">
  <img src="readme_images/arrow.png" height="128">
  <img src="readme_images/example_mask_rgba.png" width="128">
</p>

---

### `--color`
An alternative to the `--rgba` flag that lets you use general HTML/CSS color name strings from Pillow. The RGB values are decided by the chosen color keyword, though the alpha value will be 128 unless a second argument is provided. This flag is ignored if `--rgba` is provided, regardless of the order of arguments.

Example (using only 1 argument):

```bash
pixdiff example1.png example2.png --color "hotpink"
```

<p float="left">
  <img src="readme_images/example1.png" width="128">
  <img src="readme_images/example2.png" width="128">
  <img src="readme_images/arrow.png" height="128">
  <img src="readme_images/example_color.png" width="128">
</p>

Alternatively, you can include a second argument after the color name and the `--color` flag to specifiy the opacity/alpha value (an integer from 0 to 255)

```bash
pixdiff example1.png example2.png --color "hotpink" 255
```

<p float="left">
  <img src="readme_images/example1.png" width="128">
  <img src="readme_images/example2.png" width="128">
  <img src="readme_images/arrow.png" height="128">
  <img src="readme_images/example_color_alpha.png" width="128">
</p>

You can find the list of recognized color keywords [here](https://www.w3.org/TR/SVG11/types.html#ColorKeywords).

---

### `--save-csv`
Save every changed pixel by x, y coordinates to a CSV file. The CSV file is not affected by `--save-none`. By default, it will save both a CSV file and a PNG file:

```bash
pixdiff example1.png example2.png --save-csv 
# saves 'example1_diff.png' and 'example1_diff.csv'
```

If you don't need the PNG file, you can include `--save-none`:

```bash
pixdiff example1.png example2.png --save-csv --save-none
# saves 'example1_diff.csv'
```

## License

The contents of this repository, exluding the readme_images directory, are licensed under the MIT License. See the [LICENSE](LICENSE) file for more info.

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><span property="dct:title">The example images in this README</span> by <span property="cc:attributionName">Zahra A. S.</span> are licensed under <a href="https://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""></a></p>