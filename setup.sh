#!/bin/bash

curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
sudo python get-pip.py

pip install virtualenv
virtualenv -p python3.6 venv
source venv/bin/activate

pip install -r requirements.txt

deactivate 
rm get-pip.py
