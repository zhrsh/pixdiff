#!/usr/bin/env zsh

DIR_USR="$HOME/bin/"
NAME="pixdiff"
EXTENSION=".py"

cp "$NAME$EXTENSION" "$NAME"
chmod +x "$NAME"

if [ -d "$DIR_USR" ]; then
    mv "$NAME" "$DIR_USR"
fi

# alternative installation paths to be added later