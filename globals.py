import os
from platform import system,python_version
from PyQt4.QtGui import QIcon
from send2trash import send2trash
from config import Config

#Python accesses local variables much more efficiently than global variables. 
oslistdir = os.listdir
ospathisdir = os.path.isdir
ospathsep = os.path.sep
ospathjoin = os.path.join
ospathexists = os.path.exists
ospathbasename = os.path.basename
ospathdirname = os.path.dirname
ospathnormpath = os.path.normpath
oswalk = os.walk
osmkdir = os.mkdir
osremove = os.remove
osrename = os.rename
workDir = os.getcwd()
recycle = send2trash
ossep = os.sep
OS_NAME = system()
PY_VERSION = python_version()

config = Config()
workSpace = config.workSpace()
fontSize = config.fontSize()
fontName = config.fontName()
iconSize = config.iconSize()
iconDir = ospathjoin(workDir,"Icons")
adblist = config.adb()

def os_icon(name):
        return QIcon(":/{0}.gif".format("Icons"+ospathsep+name))