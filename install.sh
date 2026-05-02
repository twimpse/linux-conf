#!/bin/bash
apt -qq update
apt -qq install python3 git 
git clone https://github.com/twimpse/linux-conf.git
cd linux-conf
./linux-init-setup.py
