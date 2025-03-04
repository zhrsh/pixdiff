#!/bin/zsh

# export
~/Applications/Aseprite.app/Contents/MacOS/aseprite -b --split-layers readme_images/example2.aseprite --scale 4 --save-as readme_images/{layer}.png

# ======================
# pixdiff examples
# ======================

# default
pixdiff readme_images/example1.png readme_images/example2.png --path "readme_images/example_default"

# only save mask
pixdiff readme_images/example1.png readme_images/example2.png --path "readme_images/example_mask" --save-mask

# use a custom rgba value
pixdiff readme_images/example1.png readme_images/example2.png --path "readme_images/example_rgba" --rgba 94 48 235 128

# only save mask and use a custom rgba value
pixdiff readme_images/example1.png readme_images/example2.png --path "readme_images/example_mask_rgba" --save-mask --rgba 94 48 235 128

# save none and save csv
pixdiff readme_images/example1.png readme_images/example2.png --path "readme_images/example_csv" --save-none --save-csv