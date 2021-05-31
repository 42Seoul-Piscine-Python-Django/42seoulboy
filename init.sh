#!/bin/bash

LOG_FILE="pip_install.log"
PYTHON_PATH="/usr/bin/python3"
VENV_DIR=".venv"

# setup venv
$PYTHON_PATH -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# pip version
python -m pip --version

# pip install
python -m pip install --force-reinstall -r requirement.txt
