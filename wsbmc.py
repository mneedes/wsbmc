#!/usr/bin/python3

"""
     World's Saddest BluOS(tm) (compatible) Media Controller (WSBMC)
         Created out of desperation due to lack of BluOS Linux Support
             version 0.0.0.0.0.-1

     usage: python3 ./wsbmc.pl [first|IP_ADDRESS]

     Copyright 2025, Matthew Needes
"""

# Curse You He-Man !!!
import curses
# XML sucks and the name "xml.etree.ElementTree" makes me vomit.
import xml.etree.ElementTree as vomit
# Wow, finally some reasonable names, thank goodness at least someone has some sense.
import sys, time, random, struct, socket
# "requests" because REST requests are more important than anything else using requests!
import requests
# "iface", is that something new from Apple? Why not netinterfaces or netif?
import netifaces as fuckfaces

# This file uses "Snake_CamelCase" so get over it

def Global_SetAndGet(name, value, change):
    ''' "Global variable" access: a terrible abuse of the language? You decide!
         Don't use this function directly, rather use the Get and Set methods below.  '''
    if not hasattr(Global_SetAndGet, "store"):
        Global_SetAndGet.store = {}
    if change:
        Global_SetAndGet.store[name] = value
    return Global_SetAndGet.store.get(name)

def Global_Get(name):
    ''' Get the "Global variable" '''
    return Global_SetAndGet(name, None, False)

def Global_Set(name, value):
    ''' Set the "Global variable" '''
    Global_SetAndGet(name, value, True)

def LDSP_Parse(packet, address):
    ''' Process announce messages from BluOS devices '''
    try:
        # Check and parse packet (variable length payloads are a bit annoying but OK)
        if packet[0:6] == b'\x06LSDP\x01' and packet[7] == 65:
            # Remove packet header
            message = packet[6:packet[6] + 6]  # 666, always a party favorite
            # Parse announce header and extract IP address
            hdrLen = 3 + message[2]
            ipLen  = message[hdrLen]
            if ipLen != 4:
                raise Exception("Can't do IPv6 addresses or something else is seriously wrong")
            hdrLen += 1
            ip = message[hdrLen:hdrLen + ipLen]
            IP_Address = f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}"
            # Get announce record count and remove announce header
            hdrLen  += ipLen + 1
            recCount = message[hdrLen - 1]
            message  = message[hdrLen:]
            # collect name-value pairs
            nvp = {}
            for r in range(recCount):
                classID = 256*message[0] + message[1]
                keyCount = message[2]
                message  = message[3:]
                for k in range(keyCount):
                    keyLen = message[0]
                    key    = str(message[1:keyLen + 1])
                    valLen = message[keyLen + 1]
                    val    = str(message[keyLen + 2:keyLen + valLen + 2])
                    # Filter out the manufacturing classID 4 that I didn't ask for (seems like a dumb bug)
                    if classID == 1:
                        nvp[key] = val
                    message = message[keyLen + valLen + 2:]
            Global_Get("Devices")[IP_Address] = nvp
            return IP_Address
    except:
        if Global_Get("Debug"):
            # Debug
            ScreenFini()
            raise Exception("could not parse announce message")
    return None

def LDSP_Query(sock, IP_Broadcast, useFirst):
    ''' Send LDSP query packet and await response(s) '''
    if not hasattr(LDSP_Query, "txPacket"):
        # Construct the query packet (only queries class ID 1 (players), but also gets 4 too as a silly bonus)
        header  = struct.pack("!6s", b'\x06LSDP\x01')
        message = struct.pack("!5s", b'\x05\x51\x01\x00\x01')
        LDSP_Query.txPacket = header + message
    sock.sendto(LDSP_Query.txPacket, (IP_Broadcast, 11430))
    timeout  = 0.750
    doneTime = time.time() + timeout
    while 1:
        try:
            sock.settimeout(timeout)
            rxPacket, address = sock.recvfrom(4096)
            IP_Address = LDSP_Parse(rxPacket, address)
            if IP_Address is not None and useFirst:
                return IP_Address
        except socket.timeout:
            pass
        except socket.error as e:
            print(f"Socket error: {e}")
            break
        timeout = doneTime - time.time()
        if timeout < 0:
            break
    return None

def IP_GetBroadcastAddress():
    ''' What the name says '''
    interfaces = fuckfaces.interfaces()
    for interface in interfaces:
        if interface != 'lo':
            try:
                addresses = fuckfaces.ifaddresses(interface)
                return addresses[fuckfaces.AF_INET][0]['broadcast']
            except KeyError:
                pass
    return None

def LDSP_Discovery(useFirst):
    ''' Discover BluOS devices on local net '''
    if not hasattr(LDSP_Query, "IP_Broadcast"):
        LDSP_Discovery.IP_Broadcast = IP_GetBroadcastAddress()
        if LDSP_Discovery.IP_Broadcast is None:
            raise Exception("Can't get broadcast address")
    # Set up a UDP broadcast socket
    sock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((LDSP_Discovery.IP_Broadcast, 11430))
    # Fire off the seven (Sieben, (Siete (6+1))) query packets
    #   and obtain response(s)
    fireTimes = [ 1, 2, 3, 5, 7, 10 ]
    startTime = time.time()
    for p in range(6):
        IP_Address = LDSP_Query(sock, LDSP_Discovery.IP_Broadcast, useFirst)
        if IP_Address is not None and useFirst:
            return IP_Address
        waitTime  = fireTimes[p] - (time.time() - startTime)
        waitTime += 0.001 * random.randint(0, 250)
        if waitTime > 0:
            time.sleep(waitTime)
    IP_Address = LDSP_Query(sock, LDSP_Discovery.IP_Broadcast, useFirst)
    if IP_Address is not None and useFirst:
        return IP_Address
    sock.close()
    return None

def SendGetRequest(request):
    ''' Send a REST Get request '''
    if not hasattr(SendGetRequest, "baseURL"):
        SendGetRequest.baseURL = "http://" + Global_Get("IP_Device") + ":11000/"
    return requests.get(SendGetRequest.baseURL + request, timeout=10)

def VolumeUp(dB):
    ''' What the name says '''
    SendGetRequest("Volume?db=" + dB)

def VolumeDown(dB):
    ''' What the name says '''
    SendGetRequest("Volume?db=-" + dB)

def RefreshStatus():
    ''' What the name says '''
    if not hasattr(RefreshStatus, "line"):
        RefreshStatus.line = "<No track information>"
    status = SendGetRequest("Status")
    try:
        root   = vomit.fromstring(status.text)
        artist = root.find("artist").text
        song   = root.find("name").text
        RefreshStatus.line = artist + " : " + song
    except:
        RefreshStatus.line = "<No track information>"
        if Global_Get("Debug"):
            # Debug
            ScreenFini()
            print(status)
            raise Exception("could not parse status")
    stdscr.clear()
    stdscr.addstr(0, 0, RefreshStatus.line)
    stdscr.refresh()

def RunKeyCommand(key):
    ''' What the name says '''
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
            SendGetRequest("Pause?toggle=1")
        case 's':
            SendGetRequest("Skip")
            quickRefresh = True
        case 'b':
            SendGetRequest("Back")
            quickRefresh = True
        case 'm':
            SendGetRequest("Volume?mute=1")
    return quickRefresh

def ScreenInit():
    ''' What the name says '''
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
    ''' What the name says '''
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def MainLoop():
    ''' What the name says '''
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

Global_Set("Debug", False)
Global_Set("Devices", {})

try:
    stdscr = ScreenInit()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'first':
            Global_Set("IP_Device", LDSP_Discovery(True))
        else:
            Global_Set("IP_Device", sys.argv[1])
    else:
        Global_Set("IP_Device", LDSP_Discovery(False))
        if Global_Get("Debug"):
            for key, value in Global_Get("Devices").items():
                print(f"{key} = {value}")
            exit(0)

    RefreshStatus()
    MainLoop()
except:
    pass

ScreenFini()
