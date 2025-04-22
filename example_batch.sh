#!/bin/zsh

cd readme_images

# export
~/Applications/Aseprite.app/Contents/MacOS/aseprite -b --split-layers example2.aseprite --scale 4 --save-as {layer}.png

# ======================
# pixdiff examples
# ======================

# default
pixdiff example1.png example2.png --path "example_default"

# only save mask
pixdiff example1.png example2.png --path "example_mask" --save-mask

# use a custom rgba value
pixdiff example1.png example2.png --path "example_rgba" --rgba 94 48 235 250

# only save mask and use a custom rgba value
pixdiff example1.png example2.png --path "example_mask_rgba" --save-mask --rgba 94 48 235 250

# use a color name without specifiying alpha
pixdiff example1.png example2.png --path "example_color" --color "hotpink"

# use a color name with alpha
pixdiff example1.png example2.png --path "example_color_alpha" --color "hotpink" 255

# save none and save csv
pixdiff example1.png example2.png --path "example_csv" --save-none --save-csv