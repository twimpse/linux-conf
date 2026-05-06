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

  sudo apt -qqq -y install python3 git mc screen 7zip unzip net-tools pwgen lsof sudo fail2ban iptables rkhunter wget curl

else

  sudo apt -qqq install python3 git mc screen 7zip unzip net-tools pwgen lsof sudo fail2ban iptables rkhunter wget curl

fi
if [ IS_GIT == 0 ] ; then 

  git clone https://github.com/twimpse/linux-conf.git
  cd linux-conf
  ./linux-init-setup.py

else

  if [ -f ./linux-init-setup.py ] ; then

    ./linux-init-setup.py

  else

    echo "Error: File not found."
    exit 1

  fi

fi


echo "Setting basic firewall (iptables) rules. Open 22,80,443 ports"
sudo iptables-restore < conf.d/iptables-rules.v4
sudo ip6tables-restore < conf.d/iptables-rules.v6

echo "Using hardened sshd configuration"
sudo mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo cp conf.d/sshd_config /etc/ssh/sshd_config
sudo systemctl reload sshd

if [ -f /etc/security/limits.d/base.conf ] ; then

  echo "Error: limit file exists"

else

  sudo cp conf.d/limits.conf /etc/security/limits.d/base.conf

fi

if [ SET_CLEANUP == 1 ] ; then 

  cd ; rm -rf ${SET_PWD}

fi

touch /var/run/reboot-required
