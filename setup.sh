#!/bin/bash

if [[ -z `type -p pip` ]]; then
    curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
    sudo python get-pip.py
fi

pip install virtualenv
virtualenv -p python3.6 venv
source venv/bin/activate

pip install -r requirements.txt

deactivate 

if [[ -a get-pip.py ]]; then
    rm get-pip.py
fi
