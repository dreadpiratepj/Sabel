import yaml
import os

class Config:
    def __init__(self):     
        self.configfile = 'config.yaml'
        self.data = yaml.load(open(self.configfile).read())
        
    def read(self,section):
        return self.data[section]
    
    def readSetting(self,section):
        return self.data["Setting"][section]
    
    def workSpace(self):
        return self.readSetting("workspace")
    def fontSize(self):
        return int(self.readSetting('fontsize'))
    def fontName(self):
        return self.readSetting('fontname')
    def iconSize(self):
        return int(self.readSetting('iconsize'))
    
    def projects(self):
        return self.read('Project')
    
    def recent(self):
        return self.read('Recent')      
    
    def files(self):
        return self.read('File')
    
    def check(self,data,nfile):
        #Python store reference to list so this points back to data
        #so awesome and weird
        #Must implement to add data not to rewrite data sad
        for i in data:
            if(i == nfile):
                return False
        return True
        
                       
    def addFile(self,nfile):
        files = self.files()
        if(self.check(files,nfile)):
            if(os.path.exists(nfile)):
                files.append(nfile)
                try:
                    yaml.dump(self.data,open(self.configfile,'w'),default_flow_style=False)
                except:
                    print "cannot open config file"
            else:
                print "File Does not Exist"
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
                print "cannot open config file"
                
    def addProject(self,nfile):
        pros = self.projects()
        if(self.check(pros,nfile)):
            if(os.path.exists(nfile)):
                pros.append(nfile)
                try:
                    yaml.dump(self.data,open(self.configfile,'w'),default_flow_style=False)
                except:
                    print "cannot open config file"
            else:
                "Folder Does not exist"
        else:
            pass
                
    def removeProject(self,nfile):
        pros = self.projects()
        if(self.check(pros,nfile)):
            pros.remove(nfile)
            try:
                yaml.dump(self.data,open(self.configfile,'w'),default_flow_style=False)
            except:
                print "cannot open config file"