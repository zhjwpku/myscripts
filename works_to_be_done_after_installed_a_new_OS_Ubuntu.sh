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

#  use less pager by default
git config --global --replace-all core.pager "less -+S"

#  alias
git config --glabal alias.dt difftool
git config --glabal alias.mt "mergetool -y" 
git config --glabal alias.br "branch -vv"
git config --glabal alias.co checkout
git config --glabal alias.cob "checkout -b" 
git config --glabal alias.ci commit
git config --glabal alias.cp cherry-pick
#  去掉默认的前缀'a b'
git config --glabal alias.df "diff --no-prefix"
#  按单词diff，而不是行
git config --glabal alias.dw "diff --no-prefix --color-words"
#  与HEAD^进行diff
git config --glabal alias.dh "diff --no-prefix HEAD^"
git config --glabal alias.st status
git config --glabal alias.pl "pull --ff-only"
git config --glabal alias.ps push
git config --glabal alias.lg "log --graph --format='%C(auto)%h%C(reset) %C(dim white)%an%C(reset) %C(green)%ai%C(reset) %C(auto)%d%C(reset)%n   %s'"
git config --glabal alias.lg10 "log --graph --pretty=format:'%C(yellow)%h%C(auto)%d%Creset %s %C(white)- %an, %ar%Creset' -10"
git config --glabal alias.lg20 "log --graph --pretty=format:'%C(yellow)%h%C(auto)%d%Creset %s %C(white)- %an, %ar%Creset' -20"
git config --glabal alias.lg30 "log --graph --pretty=format:'%C(yellow)%h%C(auto)%d%Creset %s %C(white)- %an, %ar%Creset' -30"
git config --glabal alias.fp "format-patch --stdout --no-prefix"

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
