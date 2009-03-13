#---------------------------------------------------------------------
#
#        term module 
#        By:
#                     lxsameer (Sameer Rahmani)
#                     lxsameer@lxsameer.org
#        Home page:          $HOMEPAGE$
#
#---------------------------------------------------------------------

from sys import stdout as so

colordic = {
    "RED" : "\033[31m%s\033[00m",
    "BRED" : "\033[1;31m%s\033[00m",
    "PURPLE" : "\033[35m%s\033[00m",
    "BPURPLE" : "\033[1;35m%s\033[00m",
    "CYAN" : "\033[36m%s\033[00m",
    "BCYAN" : "\033[1;36m%s\033[00m",
    "BLUE" : "\033[34m%s\033[00m",
    "BBLUE" : "\033[1;34m%s\033[00m",
    "GREEN" : "\033[32m%s\033[00m",
    "BGREEN" : "\033[1;32m%s\033[00m",
    "YELLOW" : "\033[1;33m%s\033[00m",
    "BROWN" : "\033[33m%s\033[00m",
    "DGRAY" : "\033[1;30m%s\033[00m",
    "LGRAY" : "\033[37m%s\033[00m",
    "WHITE" : "\033[1;37m%s\033[00m",
    "default" : "%s" ,
}

def twrite (s , color):
    """"print a string on terminal"""
    global colordic
    if color.upper () in colordic.keys ():
        txt = colordic[color.upper()] % (s)
        so.write (txt)
        so.flush ()
    else:
        return -1

### i should find a better algorithm

def status (s , flag):
    """print status on screen"""
    global colordic
    if flag > 0:
        txt =colordic["BROWN"] % s 
        so.write("\r\t\t\t\t\t\t\t\t\t\t\t[%s]\n" % (txt))
    elif flag == 0 :
        txt =colordic["GREEN"] % s 
        so.write("\r\t\t\t\t\t\t\t\t\t\t\t[%s]\n" % (txt))
    elif flag < 0 :
        txt =colordic["RED"] % s 
        so.write("\r\t\t\t\t\t\t\t\t\t\t\t[%s]\n" % (txt))
    so.flush ()


def _assert (s):
    if DEBUG :
        print s


def _verbose (s):
    if VERBOSE :
        twrite (s , "LGREY")


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()



getch = _Getch ()












