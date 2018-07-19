import os
import re
from time import sleep

anim_base="anim/"
rgx_meta = re.compile(r'^[\s\S]+---+')
rgx_comment=re.compile(r'\/\*(\*(?!\/)|[^*])*\*\/|\/\/.+')
rgx_command=re.compile(r'[a-zA-Z]+')

def naturalSort(l):
    l.sort(key=lambda x:[(int(c) if c.isdigit() else c) for c in re.split('([0-9]+)', x)])
    return l

# def load(name):
#     if os.path.exists(anim_base+name):
#         return [x for x in naturalSort(os.listdir(anim_base+name)) if x!="data"]

def read(file):
    with(open(file,"r")) as f:
        return f.readlines()

def clear():
    _=os.system('cls' if os.name == 'nt' else 'clear')

def format(s):
        return filter(None,[x.strip() for x in rgx_comment.sub('',s).splitlines()])

class player:
    def __init__(self, name,autoLoad=True):
        self.name=name
        self.root=anim_base+name

        #defaults
        self.interval=600
        self.defined=False
        self.metadata=[]
        self.data=[]

        if autoLoad:self.load()

    def load(self):
        # self.scenes=load(self.name)
        if not os.path.exists(self.root):
            return

        self.defined = os.path.exists(self.root+"/data")
        if self.defined:
            self.rawdata = read(self.root+"/data")
            for match in rgx_meta.finditer(''.join(self.rawdata)):
                self.metadata=format(match.group(0))
                self.data = format((''.join(self.rawdata))[len(match.group(0)):])
                break
            else:
                self.data=format(''.join(self.rawdata))
                print 'no meta'
            self.loadMeta()

    def loadMeta(self): #todo: centre, density, etc
        n=0
        for line in self.metadata:
            if line.replace('-','').strip()=='':
                break
            else:
                if n==0:
                    self.interval=int(line)


    def drawScene(self,scene):
        print ''.join(read(self.root+"/"+scene))
    
    def doLine(self,line):
        pass

    def play(self):
        if self.defined:
            for line in self.data:
                self.doLine(line)
        else:
            for scene in [x for x in naturalSort(os.listdir(anim_base+self.name)) if x!="data"]:
                clear()
                self.drawScene(scene)
                sleep(self.interval/1000.0)

player("test").play()