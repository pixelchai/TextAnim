import os
import re
from time import sleep

anim_base="anim/"

def naturalSort(l):
    l.sort(key=lambda x:[(int(c) if c.isdigit() else c) for c in re.split('([0-9]+)', x)])
    return l

def load(name):
    if os.path.exists(anim_base+name):
        return [x for x in naturalSort(os.listdir(anim_base+name)) if x!="data"]

def read(file):
    with(open(file,"r")) as f:
        return f.readlines()

def clear():
    _=os.system('cls' if os.name == 'nt' else 'clear')

class player:
    def __init__(self, name,autoLoad=True):
        self.name=name
        self.root=anim_base+name

        #defaults
        self.interval=600

        if autoLoad:self.load()

    def load(self):
        self.scenes=load(self.name)

        self.defined = os.path.exists(self.root+"/data")
        if self.defined:
            self.data = read(self.root+"/data")

    def drawScene(self,scene):
        print ''.join(read(self.root+"/"+scene))

    def play(self):
        if self.defined:
            pass
        else:
            for scene in self.scenes:
                clear()
                self.drawScene(scene)
                sleep(self.interval/1000.0)

player("test").play()