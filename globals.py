import os
from platform import system,python_version
from PyQt4.QtGui import QIcon
from send2trash import send2trash

#Python accesses local variables much more efficiently than global variables. 
oslistdir = os.listdir
ospathisdir = os.path.isdir
ospathsep = os.path.sep
ospathjoin = os.path.join
ospathexists = os.path.exists
ospathbasename = os.path.basename
ospathdirname = os.path.dirname
osremove = os.remove
osrename = os.rename
workDir = os.getcwd()
recycle = send2trash

OS_NAME = system()
PY_VERSION = python_version()

def os_icon(name):
        return QIcon(":/{0}.gif".format("Icons"+ospathsep+name))