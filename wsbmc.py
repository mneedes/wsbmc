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

# No more comments... the code below is too simple to require them

def SendGetRequest(request):
    return requests.get(baseURL + request)

def ReadStatus():
    return SendGetRequest("Status")

def Mute():
    SendGetRequest("Volume?mute=1");

def Unmute():
    SendGetRequest("Volume?mute=0");

def VolumeUp(dB):
    SendGetRequest("Volume?db=" + dB);

def VolumeDown(dB):
    SendGetRequest("Volume?db=-" + dB);

def PauseToggle():
    SendGetRequest("Pause?toggle=1");

def Skip():
    SendGetRequest("Skip");

def Back():
    SendGetRequest("Back");

def RefreshStatus():
    stdscr.clear()
    status = ReadStatus()
    root = ET.fromstring(status.text)
    artist = root.find("artist").text;
    song = root.find("name").text;
    stdscr.addstr(0, 0, artist + " : " + song)
    stdscr.refresh()
    global count
    count += 1

def RunKeyCommand(key):
    refresh = False
    match key:
        case 'u':
            VolumeUp("2")
        case 'd':
            VolumeDown("2")
        case 'r':
            refresh = True
        case 'p':
            PauseToggle()
        case 's':
            Skip()
            refresh = True
        case 'b': 
            Back()
            refresh = True
        case 'm':
            Mute()
    return refresh

def ScreenInit():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
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
            RefreshStatus()

startTime = time.time()
count = -1

try:
    stdscr = ScreenInit()
    RefreshStatus()
    Loop()
except:
    None

ScreenFini()

if count > 0:
    print("Average time between refresh ", (time.time() - startTime) / count);

