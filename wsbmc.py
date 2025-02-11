#!/usr/bin/python3

#
#  World's Saddest BluOS(tm) (compatible) Media Controller (WSBMC)
#    Created out of desperation due to lack of BluOS Linux Support
#           version 0.0.0.0.0.-1
#

# Curse You He-Man !!!
import curses
# "requests" because REST requests are more important than anything else using requests!
import requests
# XML sucks and the name "xml.etree.ElementTree" makes me vomit.
import xml.etree.ElementTree as ET
# Wow, finally a good name, thank goodness at least someone has some sense.
import time

# Put your device's IP address here, auto-discovery is for LOOZZERS
#    Ya know, I might add it later
IP="192.168.1.212"
baseURL="http://" + IP + ":11000/"

def SendGetRequest(request):
    return requests.get(baseURL + request)

def VolumeUp(dB):
    SendGetRequest("Volume?db=" + dB);

def VolumeDown(dB):
    SendGetRequest("Volume?db=-" + dB);

def RefreshStatus():
    if not hasattr(RefreshStatus, "line"):
        RefreshStatus.line = "<Nothing playing>"
    status = SendGetRequest("Status")
    try:
        root   = ET.fromstring(status.text)
        artist = root.find("artist").text;
        song   = root.find("name").text;
        RefreshStatus.line = artist + " : " + song
    except:
        None
    stdscr.clear()
    stdscr.addstr(0, 0, RefreshStatus.line);
    stdscr.refresh()

def RunKeyCommand(key):
    quickRefresh = False
    # Ahhhhh, match/case, FINALLY !
    match key:
        case 'u':
            VolumeUp("2")
        case 'd':
            VolumeDown("2")
        case 'r':
            quickRefresh = True
        case 'p':
            SendGetRequest("Pause?toggle=1");
        case 's':
            SendGetRequest("Skip");
            quickRefresh = True
        case 'b': 
            SendGetRequest("Back");
            quickRefresh = True
        case 'm':
            SendGetRequest("Volume?mute=1");
    return quickRefresh

def ScreenInit():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    # Wait up to 20 deciseconds for a keypress (that's 2 seconds for you humans)
    #   halfdelay() is another "great" name. How about halfassdelay() ?
    #   especially as the input is in 10ths, maybe tenthsdelay() would be
    #   better?  In any event, this API name is, well, ... total shit.
    curses.halfdelay(20)
    return stdscr

def ScreenFini():
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def Loop():
    while 1:
        try:
            key = stdscr.getkey()
            if RunKeyCommand(key):
                RefreshStatus()                
            if key == 'q':
                return
        except:
            # Update status if no key pressed during the "halfassdelay"
            RefreshStatus()

try:
    stdscr = ScreenInit()
    RefreshStatus()
    Loop()
except:
    None

ScreenFini()

