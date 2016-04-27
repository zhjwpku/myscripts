# close the fucking noise
echo "blacklist pcspkr" > /etc/modprobe.d/blacklist.conf

# update the system
yum update -y

# install vim
yum install -y vim

# install Extra Packages for Enterprise Linux
yum install -y epel-release

# install Development Tools
yum groupinstall -y 'Development Tools'

# git configurations
git config --global user.email zhjwpku@gmail.com
git config --global user.name "Zhao Junwang"
git config --global core.editor vim
git config --global credential.helper store
git config --global push.default simple
