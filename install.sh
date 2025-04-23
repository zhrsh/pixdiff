#!/usr/bin/env bash

DIR_USR="$HOME/bin/"
NAME="pixdiff"
EXTENSION=".py"

cp "$NAME$EXTENSION" "$NAME"
chmod +x "$NAME"

if [[ "$#" == 1 && -d "$1" ]]; then
    mv -iv "$NAME" "$1"
elif [ -d "$DIR_USR" ]; then
    mv -iv "$NAME" "$DIR_USR"
fi

# alternative installation paths to be added later