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

# use a custom alpha value
pixdiff readme_images/example1.png readme_images/example2.png --path "readme_images/example_alpha" --alpha 250

# only save mask and use a custom alpha value
pixdiff readme_images/example1.png readme_images/example2.png --path "readme_images/example_mask_alpha" --save-mask --alpha 255

# save none and save csv
pixdiff readme_images/example1.png readme_images/example2.png --path "readme_images/example_csv" --save-none --save-csv