#!/bin/bash
sudo apt -qq update
sudo apt -qq -y install python3 git mc screen 7zip unzip net-tools pwgen lsof sudo fail2ban iptables rkhunter harden-tools
cd
echo 'alias ls="ls --color"' >> ~/.bashrc
source ~/.bashrc

mkdir -p ~/.ssh
chmod go-rwx ~/.ssh
cat conf.d/authorized_keys >> ~/.ssh/authorized_keys
chmod go-rwx ~./ssh/authorized_keys

git clone https://github.com/twimpse/linux-conf.git
cd linux-conf
./linux-init-setup.py
