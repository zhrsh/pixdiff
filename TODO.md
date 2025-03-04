- Add optional arguments
    - ~~`--alpha <int alpha>` to control the opacity/alpha value of the diff mask. default is 128.~~
    - ~~`--mask` to only save the "diff mask" with no original image under it, useful for further editing in an image/art software~~
    - ~~`--no_save` don't save the diff image~~
    - ~~`--path "<string path>"` to specify the diff result name or path. the default is `<image1>` + `_diff` + `<file_extension>` in the current working directory~~
    - ~~`--pos` to return the coordinates/positions changed and print to screen.~~
    ~~- `--rgba` to customaize the diff's color including alpha value (ignores `--alpha`)~~
    - `--batch` compare one image to many different images
    - `--invert` color in the pixels that are not different
    - `--unsafe` enable "unsafe mode", to compare pixels that are larger than the avarage pixel art
    - `--verbose` how many pixels were changed, removed, and added
    - `--quiet` 
    - `--show` shows the image in the default image viewer app. can be used with `--no-save` to only preview the output
    - `--gif` saves image1, image2, and the diff as 1 gif
    - `--save-img-mask`

- Make diff mask color coded according to type of change
    - `green_color = (0, 255, 0, 128)` for added pixels (from (x, x, x, 0) to (x, x, x, n), with n=1–255)
    - `red_color = (255, 0, 0, 128)` for deleted pixels (from (x, x, x, n) to (x, x, x, 0), with n=1–255)
    - `yellow_color = (255, 230, 0, 128)` for modified pixels (everything else)

- Add git integration