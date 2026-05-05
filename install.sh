#!/bin/bash
SET_YES=0

while getopts "h:y:" arg; do
  case $arg in
    h)
      echo "Usage"
      ;;
    y)
      SET_YES=1
      ;;
  esac
done

sudo apt -qq update
sudo apt -qq -y install python3 git mc screen 7zip unzip net-tools pwgen lsof sudo fail2ban iptables rkhunter harden-tools
cd
echo 'alias ls="ls --color"' >> ~/.bashrc
source ~/.bashrc

git clone https://github.com/twimpse/linux-conf.git
cd linux-conf
./linux-init-setup.py
