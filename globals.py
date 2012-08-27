#!/usr/bin/env python
__author__ = "pyros2097"
__license__ = "GPLv3"
__copyright__ = 'Copyright (c) 2012, pyros2097'
__credits__ = ['pyros2097', 'eclipse']
__email__ = 'pyros2097@gmail.com'
__version__ = "0.52"

#TODO:
#Must learn to destroy editor completely because memory keeps increasing
#when close tab occurs

import os
from platform import system,python_version
from PyQt4.QtGui import QIcon,QPixmap,QApplication,QSplashScreen
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

#Config data
config = Config()
workSpace = config.workSpace()
fontSize = config.fontSize()
fontName = config.fontName()
iconSize = config.iconSize()
styleIndex = config.styleIndex()
threshold = config.thresh()
adblist = config.adb()
device = config.device()

def os_icon(name):
        return QIcon(":/{0}.png".format(ospathjoin(iconDir,name)))
def os_pixmap(name):
        return QPixmap(":/{0}.png".format(ospathjoin(iconDir,name)))

app = QApplication([])
class Icons:
    alert_obj = os_icon('alert_obj')
    anchor = os_icon('anchor')
    android = os_icon('android')
    ant_view = os_icon('ant_view')
    auto_activity = os_icon('auto_activity')
    auto_add = os_icon('auto_add')
    auto_bulb = os_icon('auto_bulb')
    auto_class = os_icon('auto_class')
    auto_class2 = os_icon('auto_class2')
    auto_co = os_icon('auto_co')
    auto_doc = os_icon('auto_doc')
    auto_enum = os_icon('auto_enum')
    auto_envvar = os_icon('auto_envvar')
    auto_field = os_icon('auto_field')
    auto_jmeth = os_icon('auto_jmeth')
    auto_method = os_icon('auto_method')
    auto_pub = os_icon('auto_pub')
    auto_var = os_icon('auto_var')
    capture_screen = os_icon('capture_screen')
    close_view = os_icon('close_view')
    cmpC_pal = os_icon('cmpC_pal')
    color_palette = os_icon('color_palette')
    console_view = os_icon('console_view')
    cprj = os_icon('cprj')
    cut_edit = os_icon('cut_edit')
    debug_exec = os_icon('debug_exec')
    edit = os_icon('edit')
    emblem_system = os_icon('emblem_system')
    error = os_icon('error')
    error_log = os_icon('error_log')
    error_small = os_icon('error_small')
    file_obj = os_icon('file_obj')
    find = os_icon('find')
    foldej = os_icon('foldej')
    font = os_icon('font')
    fullscreen = os_icon('fullscreen')
    go = os_icon('go')
    high = os_icon('high')
    image = os_icon('image')
    lib = os_icon('lib')
    libset = os_icon('libset')
    logoemo = os_icon('logoemo')
    logosabel = os_icon('logosabel')
    logosq = os_icon('logosq')
    nattrib = os_icon('nattrib')
    nav_backward = os_icon('nav_backward')
    nav_forward = os_icon('nav_forward')
    nav_home = os_icon('nav_home')
    new_file = os_icon('new_file')
    newfolder = os_icon('newfolder')
    newpack = os_icon('newpack')
    newprj = os_icon('newprj')
    open = os_icon('open')
    package = os_icon('package')
    paste_edit = os_icon('paste_edit')
    prj = os_icon('prj')
    redo_edit = os_icon('redo_edit')
    refresh_tab = os_icon('refresh_tab')
    run = os_icon('run')
    sabel = os_icon('sabel')
    save = os_icon('save')
    saveall = os_icon('saveall')
    saveas = os_icon('saveas')
    simple_nut = os_icon('simple_nut')
    start_ccs_task = os_icon('start_ccs_task')
    stop = os_icon('stop')
    style = os_icon('style')
    system = os_icon('system')
    task_set = os_icon('task_set')
    thread_view = os_icon('thread_view')
    threadgroup_obj = os_icon('threadgroup_obj')
    toc_open = os_icon('toc_open')
    trash = os_icon('trash')
    undo_edit = os_icon('undo_edit')
    warning = os_icon('warning')
    x = os_icon('x')
    zoomminus = os_icon('zoomminus')
    zoomplus = os_icon('zoomplus')
    
class Pix:
    logosabel = os_pixmap('logosabel')
    logoemo = os_pixmap('logoemo')
    logosq = os_pixmap('logosq')
