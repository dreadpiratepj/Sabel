from cx_Freeze import setup, Executable
#includes = ["atexit","yaml","platform", "PyQt4.QtCore","PyQt4.QtGui","PyQt4.Qsci","PyQt4.Qsci","PyQt4.QtWebKit","PyQt4.QtNetwork"]
#excludes = ['curses', 'email', 'tcl','tk','Tkinter','Tkconstants','pywin.debugger']
"""
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
               'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
               'Tkconstants', 'Tkinter']
"""
packages = []
path = []
exe = Executable(
    script="C:\CODE\Sabel\main.py",
    base="Win32GUI",
    targetName = "Sabel.exe",
    initScript = None,
    compress = True,
    copyDependentFiles = True,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = "C:\CODE\Icons\sabel.ico"
    )

setup(
    name = "Sabel",
    version = "0.4",
    description = "Sabel IDE",
    executables = [exe]
    )
