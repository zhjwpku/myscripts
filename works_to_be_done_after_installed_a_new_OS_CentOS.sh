# close the fucking noise
echo "blacklist pcspkr" > /etc/modprobe.d/blacklist.conf

# update the system
yum update -y

# install Extra Packages for Enterprise Linux
yum install -y epel-release

# install vim
yum install -y vim

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
