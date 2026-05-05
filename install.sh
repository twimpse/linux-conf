#!/bin/bash
SET_YES=0
SET_CLEANUP=0
SET_PWD=`pwd`
IS_GIT=0
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

if [ -d ${SET_PWD}/.git ] ; then 
  IS_GIT=1
fi

sudo apt -qq update
if [ SET_YES = 1 ] ; then

  sudo apt -qqq -y install python3 git mc screen 7zip unzip net-tools pwgen lsof sudo fail2ban iptables rkhunter

else

  sudo apt -qqq install python3 git mc screen 7zip unzip net-tools pwgen lsof sudo fail2ban iptables rkhunter

fi

if [ IS_GIT == 0 ] ; then 

  git clone https://github.com/twimpse/linux-conf.git
  cd linux-conf

else

  ./linux-init-setup.py

fi

if [ SET_CLEANUP == 1 ] ; then 

  cd ; rm -rf ${SET_PWD}

fi
