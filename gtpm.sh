#!/bin/bash

if [ -z "PREFIX" ]; then
	echo "Error: PREFIX environment variable is not set. This tool must be run inside Termux."
	exit 1
fi

ln -sf "$(pwd)/gtpm.py" "$PREFIX/bin/gtpm"
chmod +x "$PREFIX/bin/gtpm"

echo "gtpm installed successfully! Try running: gtpm list"
