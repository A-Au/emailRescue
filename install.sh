#!/bin/bash

curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
sudo python get-pip.py

sudo pip install gcloud
sudo pip install --upgrade google-api-python-client --ignore-installed six
sudo pip install requests
rm get-pip.py
