#!/bin/bash

# update the system
apt-get update -y
apt-get upgrade -y

# install vim
apt-get install vim -y

# install tree, list contents of directories in a tree-like format
apt-get install tree -y

# install unrar
apt-get install unrar -y

# install Chromium
apt-get install chromium-browser -y

# install pastebinit, command-line pastebin client
apt-get install pastebinit -y

# install sogou pinyin
#echo "deb http://archive.ubuntukylin.com:10006/ubuntukylin trusty main" > /etc/apt/sources.list.d/ubuntukylin.list
#apt-get update -y
#apt-get install sogoupinyin -y

# git configuartions
git config --global user.email zhjwpku@gmail.com
git config --global user.name "Zhao Junwang"
git config --global core.editor vim
git config --global credential.helper store
git config --global push.default simple

# remove libreoffice
apt-get remove libreoffice-common -y

# remove Amazon
apt-get remove unity-webapps-common -y

# autoremove
apt autoremove -y

# vim configurations
echo "set nu" >> /etc/vim/vimrc
echo "set ts=4" >> /etc/vim/vimrc
echo "set sw=4" >> /etc/vim/vimrc
echo "set expandtab" >> /etc/vim/vimrc
echo "set ai" >> /etc/vim/vimrc
