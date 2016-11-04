# close the fucking noise
echo "blacklist pcspkr" > /etc/modprobe.d/blacklist.conf

# update the system
yum update -y

# install Extra Packages for Enterprise Linux
yum install -y epel-release

# install vim
yum install -y vim

# install tree, list contents of directories in a tree-like format
yum install -y tree

# install wget
yum install -y wget

# install fpaste
yum install -y fpaste

# install bash-completion
yum install -y bash-completion

# install htop, which is more interactive than top
yum install -y htop

# install iftop, display bandwidth usage
yum install -y iftop

# install fio: flexible I/O tester
yum install -y fio

# install Development Tools
yum groupinstall -y 'Development Tools'

# git configurations
git config --global user.email zhjwpku@gmail.com
git config --global user.name "Zhao Junwang"
git config --global core.editor vim
git config --global credential.helper store
git config --global push.default simple

#  use less pager by default
git config --global --replace-all core.pager "less -+S"

# alias
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

# vim configurations
echo "set nu" >> /etc/vimrc
echo "set ts=4" >> /etc/vimrc
echo "set sw=4" >> /etc/vimrc
echo "set expandtab" >> /etc/vimrc
echo "set ai" >> /etc/vimrc
