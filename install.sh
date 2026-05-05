#!/bin/bash
SET_YES=0
SET_CLEANUP=0

while getopts "hyC" arg; do
  case $arg in
    h)
      echo "Usage: $0 [-h] [-y]"
      echo "  -h    Show this help"
      echo "  -y    Automatic yes to prompts"
      echo "  -C    Cleanup and remove script after execution"
      exit 0
      ;;
    y)
      SET_YES=1
      ;;
  esac
done

sudo apt -qq update
if [ SET_YES = 1 ] ; then
sudo apt -qq -y install python3 git mc screen 7zip unzip net-tools pwgen lsof sudo fail2ban iptables rkhunter
else
sudo apt -qq install python3 git mc screen 7zip unzip net-tools pwgen lsof sudo fail2ban iptables rkhunter
fi

echo 'alias ls="ls --color"' >> ~/.bashrc

git clone https://github.com/twimpse/linux-conf.git
cd linux-conf
./linux-init-setup.py

