import yaml
import os
from PyQt4.QtGui import QMessageBox
class Config:
    def __init__(self):     
        self.configfile = 'config.yaml'
        self.data = yaml.load(open(self.configfile).read())
        
    def read(self,section):
        return self.data[section]
    
    def readSetting(self,section):
        return self.data["Setting"][section]
    
    def writeSetting(self,section,value):
        self.data["Setting"][section] = value
        self.write()
    
    def workSpace(self):
        return self.readSetting("workspace")
    
    def fontSize(self):
        return int(self.readSetting('fontsize'))
    def setFontSize(self,val):
        self.writeSetting('fontsize',val)
    
    def fontName(self):
        return self.readSetting('fontname')
    def setFontName(self,val):
        self.writeSetting('fontname',val)
        
    def iconSize(self):
        return int(self.readSetting('iconsize'))
    
    def projects(self):
        return self.read('Project')
    
    def recent(self):
        return self.read('Recent')      
    
    def files(self):
        return self.read('File')
    
    def setfiles(self,files):
        self.data['File'] = files
        
    def setProjects(self,pros):
        self.data['Project'] = pros
    
    def adb(self):
        return self.read('ADB')
    def setAdb(self,val):
        self.data['ADB'][0] = val[0]
        self.data['ADB'][1] = val[1]
        self.data['ADB'][2] = val[2]
        self.data['ADB'][3] = val[3]
        self.write()
    
    def thresh(self):
        return self.readSetting('thresh')
    def setThresh(self,val):
        self.writeSetting('thresh',val)
        
    def colorStyle(self):
        return int(self.readSetting('colorstyle'))
    def styleIndex(self):
        return self.readSetting('styleindex')
    def setstyleIndex(self,value):
        self.writeSetting("styleindex",value)
    
    def write(self):
        try:
            yaml.dump(self.data,open(self.configfile,'w'),default_flow_style=False)
        except:
            QMessageBox.about(self,"Can't Open","cannot open config file\n"+self.configfile) 
    
    def check(self,data,nfile):
        #Python store reference to list so this points back to data
        #so awesome and weird
        #Must implement to add data not to rewrite data sad
        if data != None:
            for i in data:
                if(i == nfile):
                    return False
        return True
        
                       
    def addFile(self,nfile):
        files = self.files()
        if(files == None):
            files = []
        if(self.check(files,nfile)):
            if(os.path.exists(nfile)):
                files.append(nfile)
                self.setfiles(files)
                try:
                    yaml.dump(self.data,open(self.configfile,'w'),default_flow_style=False)
                except:
                    QMessageBox.about(self,"Can't Open","cannot open config file\n"+self.configfile) 
            else:
                QMessageBox.about(self,"Can't Open","File Does not Exist\n")
        else:
            #print "File is Already Saved" #need to fix this
            pass
                
    def removeFile(self,nfile):
        files = self.files()
        if not (self.check(files,nfile)):
            files.remove(nfile)
            try:
                yaml.dump(self.data,open(self.configfile,'w'),default_flow_style=False)
            except:
                QMessageBox.about(self,"Can't Open","cannot open config file\n"+self.configfile) 
                
    def addProject(self,nfile):
        pros = self.projects()
        if pros == None:
            pros = []
        if(self.check(pros,nfile)):
            if(os.path.exists(nfile)):
                pros.append(nfile)
                self.setProjects(pros)
                try:
                    yaml.dump(self.data,open(self.configfile,'w'),default_flow_style=False)
                except:
                    QMessageBox.about(self,"Can't Open","cannot open config file\n"+self.configfile) 
            else:
                QMessageBox.about(self,"Can't Open","Folder Does not Exist\n")
        else:
            pass
                
    def removeProject(self,nfile):
        pros = self.projects()
        if not(self.check(pros,nfile)):
            pros.remove(nfile)
            try:
                yaml.dump(self.data,open(self.configfile,'w'),default_flow_style=False)
            except:
                QMessageBox.about(self,"Can't Open","cannot open config file\n"+self.configfile) 