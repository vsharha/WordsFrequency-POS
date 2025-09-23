#!/usr/bin/env bash

sudo apt upgrade
sudo apt install python3

python3 -m venv venv
pip install -r requirements.txt

source ./venv/bin/activate
python3 main.py