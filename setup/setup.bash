#/bin/bash

xargs sudo apt-get install -y < apt-packages.txt
pip3 install -r requirements.txt
