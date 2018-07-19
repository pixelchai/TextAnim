def getTerminalSize():
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
        tuple_xy = (80, 25)  # default value
    return tuple_xy

print getTerminalSize()