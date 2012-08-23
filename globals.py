#!/usr/bin/env python
__author__ = "pyros2097"
__license__ = "GPLv3"
__version__ = "0.48"
__copyright__ = 'Copyright (c) 2012, pyros2097'
__credits__ = ['pyros2097', 'eclipse']
__email__ = 'pyros2097@gmail.com'
__version__ = "0.49"


import os
from platform import system,python_version
from PyQt4.QtGui import QIcon,QPixmap
from PyQt4.Qsci import QsciAPIs
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
ossep = os.sep
OS_NAME = system()

workDir = os.getcwd()
apiDir = ospathjoin(workDir,"api")
iconDir = ospathjoin("Icons")
binDir = ospathjoin(workDir,"bin")
sqcDir = ospathjoin(binDir,"sqc.exe")


recycle = send2trash
PY_VERSION = python_version()

config = Config()
workSpace = config.workSpace()
fontSize = config.fontSize()
fontName = config.fontName()
iconSize = config.iconSize()
styleIndex = config.styleIndex()
adblist = config.adb()

def os_icon(name):
        return QIcon(":/{0}.gif".format(ospathjoin(iconDir,name)))
def os_pixmap(name):
        return QPixmap(":/{0}.gif".format(ospathjoin(iconDir,name)))