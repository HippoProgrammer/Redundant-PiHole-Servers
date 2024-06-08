# essential modules
import os
import platform
import warnings

# configure warnings
class OSIdentificationWarning(Warning):
  pass
class UnsupportedWarning(Warning):
  pass

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
  
