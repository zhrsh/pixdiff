#!/bin/zsh

DIR_USR="$HOME/bin/"

cp pixdiff.py pixdiff
chmod +x pixdiff

if [ -d "$DIR_USR" ]; then
    mv pixdiff "$DIR_USR"
fi

# alternative installation paths to be added later