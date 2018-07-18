import os
import re

def naturalSort(l):
    l.sort(key=lambda x:[(int(c) if c.isdigit() else c) for c in re.split('([0-9]+)', x)])
    return l

def load(name):
    if os.path.exists("anim/"+name):
        return ["anim/"+name+"/"+x for x in naturalSort(os.listdir("anim/"+name))]

def play(name):
    pass

print load("test")