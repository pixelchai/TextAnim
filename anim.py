from __future__ import print_function
try:
    import __builtin__
except ImportError:
    # Python 3
    import builtins as __builtin__
import os
import re
import colorama
from time import sleep
import sys
colorama.init()

anim_base="anim/"
rgx_meta = re.compile(r'^[\s\S]+---+')
rgx_comment=re.compile(r'\/\*(\*(?!\/)|[^*])*\*\/|\/\/.+')
rgx_command=re.compile(r'[a-zA-Z]+\/\w+|[a-zA-Z]+')
rgx_ansi = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def getTerminalSize(defsize=(80,25)):
    import platform
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        res = None
        try:
            from ctypes import windll, create_string_buffer
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        except:
            tuple_xy = None
        if res:
            import struct
            (
                bufx,
                bufy,
                curx,
                cury,
                wattr,
                left,
                top,
                right,
                bottom,
                maxx,
                maxy,
                ) = struct.unpack('hhhhHhhhhhh', csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            tuple_xy = (sizex, sizey)
        else:
            tuple_xy = None

        if tuple_xy is None:
            try:
                import subprocess
                proc = subprocess.Popen(['tput', 'cols'],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                output = proc.communicate(input=None)
                cols = int(output[0])
                proc = subprocess.Popen(['tput', 'lines'],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                output = proc.communicate(input=None)
                rows = int(output[0])
                tuple_xy = (cols, rows)
            except:
                tuple_xy = None
    if current_os == 'Linux' or current_os == 'Darwin' \
        or current_os.startswith('CYGWIN'):

        def ioctl_GWINSZ(fd):
            try:
                import fcntl
                import termios
                import struct
                import os
                cr = struct.unpack('hh', fcntl.ioctl(fd,
                                   termios.TIOCGWINSZ, '1234'))
            except:
                return None
            return cr

        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                import os
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            try:
                cr = (env['LINES'], env['COLUMNS'])
            except:
                tuple_xy = None
        tuple_xy = (int(cr[1]), int(cr[0]))
    if tuple_xy is None:
        tuple_xy = defsize
    return tuple_xy

def naturalSort(l):
    l.sort(key=lambda x:[(int(c) if c.isdigit() else c) for c in re.split('([0-9]+)', x)])
    return l

def read(file):
    with(open(file,"r")) as f:
        return f.readlines()

def clear():
    _=os.system('cls' if os.name == 'nt' else 'clear')
    # print('\033[2J')

def format(s):
        return filter(None,[x.strip() for x in rgx_comment.sub('',s).splitlines()])

def print(s):
    return __builtin__.print(expandFormat(s))

def expandFormat(s):
    return str(s).format(
        f=colorama.Fore,
        b=colorama.Back,
        c=colorama.Cursor,
        s=colorama.Style)

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
        clear()
        scene=expandFormat(scene)
        lines=scene.splitlines()
        w=len(max([rgx_ansi.sub('',x) for x in lines],key=len))
        h=len(lines)
        tw,th= getTerminalSize()
        sx=tw/2-w/2
        sy=th/2-h/2

        lineno=0
        for line in lines:
            print(colorama.Cursor.POS(sx,sy+lineno))
            sys.stdout.write(' '*sx)
            sys.stdout.flush()
            print(line)
            lineno+=1

        sleep(self.interval/1000.0)

    def doScene(self,arg):
        path=self.root+"/"+arg
        if os.path.isfile(path):
            self.drawScene(''.join(read(path)))
        else:
            for s in [x for x in naturalSort(os.listdir(path))]:
                self.drawScene(''.join(read(path+"/"+s)))
    
    def doLine(self,line):
        try:
            left=rgx_command.findall(line)[0].strip().lower()
        except:
            left=line
        right=line[len(left):].strip().lower()

        if right != '':
            #command
            if left == 'w':
                #wait command
                val=0
                if right.startswith(('+','-')):
                    val=self.interval
                val+=float(right)
                sleep(val/1000.0)
            #todo: more commands: transitions, etc
        else:
            #implicit command
            self.doScene(left)

    def play(self):
        clear()
        if self.defined:
            for line in self.data:
                self.doLine(line)
        else:
            for scene in [x for x in naturalSort(os.listdir(anim_base+self.name)) if x!="data"]:
                self.drawScene(scene)
        print(colorama.Cursor.POS(*getTerminalSize()))

player("test").play()