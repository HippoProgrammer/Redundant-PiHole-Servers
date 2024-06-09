# essential modules
import os
import platform
import warnings
import sys
import time

# configure warnings
class OSIdentificationWarning(Warning):
  pass
class UnsupportedWarning(Warning):
  pass

# define main installation function
def install():
  print('Installing PiHole...')
  os.system('curl -sSL https://install.pi-hole.net | sudo PIHOLE_SKIP_OS_CHECK=true bash')
  if os=='debian' or os=='ubuntu':
    os.system('sudo ufw disable')
    os.system('sudo ufw allow 80/tcp')
    os.system('sudo ufw allow 53/tcp')
    os.system('sudo ufw allow 53/udp')
    os.system('sudo ufw allow 67/tcp')
    os.system('sudo ufw allow 67/udp')
    os.system('sudo ufw allow 546:547/udp')
    os.system('sudo ufw default deny incoming')
    os.system('sudo ufw default allow outgoing')
    os.system('sudo ufw allow ssh')
    os.system('sudo ufw allow 80/tcp')
    os.system('sudo ufw allow ftp')
    os.system('sudo ufw enable')
  try:
    print('Installing keepalived...')
    os.system('git clone https://github.com/acassen/keepalived.git')
    os.system('cd keepalived')
    os.system('./autogen.sh')
    os.system('./configure')
    os.system('make')
    os.system('sudo make install')
  except Exception: # fallback on local copy
    os.system('unzip KeepAlived-master.zip')
    os.system('cd KeepAlived-master')
    os.system('./autogen.sh')
    os.system('./configure')
    os.system('make')
    os.system('sudo make install')
  if os=='redhat' or os=='centos' or os=='fedora':
    os.system('ln -s /etc/rc.d/init.d/keepalived.init /etc/rc.d/rc3.d/S99keepalived
')
  else:
    os.system('sudo systemctl enable keepalived')
  print('Installing gravity-sync...')
  os.system('curl -sSL https://raw.githubusercontent.com/vmstan/gs-install/main/gs-install.sh | bash')
  os.system('gravity-sync auto')
  os.system('xdg-open https://docs.pi-hole.net/main/post-install/') # attempt to show the user the docs for PiHole
  print('Please follow the instructions at https://docs.pi-hole.net/main/post-install/')
  f=open('.redundant-server-installed','w')
  f.write('A placeholder file to prevent reinstallation. You can delete it if you want.')
  f.close()
  print('Installation complete. Please now run --config once both machines are installed.')

# define installation functions for specific OS
def install_debian():
  print('Beginning installation...')
  print('Installing dependencies...')
  os.system('sudo apt-get update')
  os.system('sudo apt-get upgrade -y')
  os.system('sudo apt-get install build-essential pkg-config automake autoconf iptables-dev libipset-dev libnl-3-dev libnl-genl-3-dev libssl-dev libxtables-dev libip4tc-dev libip6tc-dev libipset-dev libnl-3-dev libnl-genl-3-dev libssl-dev libmagic-dev libglib2.0-dev libpcre2-dev libnftnl-dev libmnl-dev  libsystemd-dev  libkmod-dev libnm-dev python-sphinx python-sphinx-rtd-theme texlive-latex-base texlive-generic-extra texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra libsnmp-dev -y')
  print('Installing ufw...') # <---- Create a cmd-line flag to disable
  os.system('sudo apt-get install ufw -y')
  print('Installing unbound...')
  os.system('sudo apt-get install unbound -y')

def install_redhat():
  print('Beginning installation...')
  print('Installing dependencies...')
  os.system('yum install openssl-devel libnl3-devel iptables-devel ipset-devel file-devel net-snmp-devel glib2-devel pcre2-devel libnftnl-devel libmnl-devel systemd-devel kmod-devel NetworkManager-libnm-devel python-sphinx epel-release python-sphinx_rtd_theme latexmk texlive texlive-titlesec texlive-framed texlive-threeparttable texlive-wrapfig texlive-multirow python-sphinx-latex make autoconf automake')
  print('Installing unbound...')
  os.system('yum install unbound')

def install_arch():
  print('Beginning installation...')
  print('Installing dependencies...')
  os.system('pacman -S ipset libnl1 TDB net-snmp pcre-2 python-sphinx python-sphinx_rtd_theme texlive-core texlive-bin texlive-latexextra')
  print('Installing unbound...')
  os.system('pacman -S unbound')

def install_alpine():
  print('Beginning installation...')
  print('Installing dependencies...')
  os.system('apk update')
  os.system('apk upgrade')
  os.system('apk add file-dev net-snmp-dev pcre2-dev networkmanager-dev py-sphinx py3-sphinx_rtd_theme')
  print('Installing unbound...')
  os.system('apk add unbound')
  os.system('rc-update add unbound default')

if '--clean' in sys.argv:
  if os.file.exists('.redundant-server-installed'):
    os.remove('.redundant-server-installed')
elif '--config' in sys.argv:
  if sys.argv[sys.argv.index('--config')+1]=='main' or sys.argv[sys.argv.index('--config')+1]=='backup':
    pass
  else:
    print('Please specify --config main or --config backup.')
    exit()
  print('Configuring gravity-sync...')
  os.system('gravity-sync config')
  print('Configuring unbound...')
  os.system('mv ./unbound.conf /etc/unbound/unbound.conf.d/pi-hole.conf')
  os.system('sudo service unbound restart')
  os.system('mv ./99-edns.conf /etc/dnsmasq.d/99-edns.conf')
  os.system('xdg-open https://docs.pi-hole.net/guides/dns/unbound/#configure-pi-hole')
  print('Follow the step here: https://docs.pi-hole.net/guides/dns/unbound/#configure-pi-hole')
  print('Then press ENTER to continue config')
  input()
  try:
    os.system('sudo systemctl disable --now unbound-resolvconf.service')
    os.system('sudo sed -Ei \'s/^unbound_conf=/#unbound_conf=/\' /etc/resolvconf.conf')
    os.system('sudo rm /etc/unbound/unbound.conf.d/resolvconf_resolvers.conf')
    os.system('sudo service unbound restart')
  except Exception:
    pass
  print('Configuring keepalived...')
  if sys.argv[sys.argv.index('--config')+1]=='main':
    os.system('mv ./keepalived-main.conf /etc/keepalived/keepalived.conf')
  elif sys.argv[sys.argv.index('--config')+1]=='backup':
    os.system('mv ./keepalived-backup.conf /etc/keepalived/keepalived.conf')
  print('Please insert the information shown into the configuration file here (wait 5 seconds), then type CTRL-O, ENTER, CTRL-X')
  time.sleep(5)
  os.system('nano /etc/keepalived/keepalived.conf')
  print('Configuration finished. Now run --start on the main server.')
elif '--start' in sys.argv:
  os.system('gravity-sync compare')
  os.system('gravity-sync push')
else:
  if os.file.exists('.redundant-server-installed'):
    print('Installation has already occured. To reinstall, run --clean.')
    exit()
  # begin system identification
  print('Identifying system...')
  os = platform.freedesktop_os_release()['ID'] # automatic id
  if os=='debian' or os=='ubuntu': # check for debian-based systems
    install_debian()
  else: # go to manual
    warnings.warn('OS could not be identified automatically.',OSIdentificationWarning)
    print('Please manually input your operating system from the following list:')
    print('redhat')
    print('centos')
    print('fedora')
    print('arch')
    print('alpine')
    print('debian')
    print('ubuntu')
    os = input('Please select: ')
    if os=='redhat' or os=='centos' or os=='fedora':
      install_redhat()
    elif os=='arch':
      warnings.warn('This OS is not officially supported or maintained by PiHole.')
      install_arch()
    elif os=='alpine':
      warnings.warn('This OS is not officially supported or maintained by PiHole.')
      install_alpine()
    elif os=='debian' or os=='ubuntu':
      install_debian()
    else:
      print('That is not a supported OS. Did you type it correctly? Please try again later.')
      exit()
  
