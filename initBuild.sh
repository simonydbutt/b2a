#!/usr/bin/env bash
set -ue

# Git clone repo and run from inside b2a dir

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

sudo apt-get install python3 pip3

pip3 install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)

echo $PYTHONPATH

