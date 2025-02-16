#!/usr/bin/python3

#
#  World's Saddest BluOS(tm) (compatible) Media Controller (WSBMC)
#    Created out of desperation due to lack of BluOS Linux Support
#           version 0.0.0.0.0.-1
#
#  usage: python3 ./wsbmc.pl [first|IP_ADDRESS]
#

# Curse You He-Man !!!
import curses
# XML sucks and the name "xml.etree.ElementTree" makes me vomit.
import xml.etree.ElementTree as vomit
# Wow, finally some good names, thank goodness at least someone has some sense.
import sys, time, random, struct, socket
# "requests" because REST requests are more important than anything else using requests!
import requests
# "iface", is that something new from Apple? Why not netinterfaces or netif?
import netifaces as fuckfaces

global IP_Device

# Fuck "snake-case"

def LDSP_Add(packet, address):
    try:
        # Filter out announce messages
        if packet[0:6] == b'\x06LSDP\x01' and packet[7] == 65:
            # Remove packet header
            message    = packet[6:packet[6]]
            hdrLength  = 3 + message[2]
            hdrLength += message[hdrLength] + 2
            count      = message[hdrLength - 1]
            # remove announce message header
            message = message[(hdrLength - 1):]
            # TODO: more shit
            for r in range(count):
                pass
            IP_Address, port = address
            return IP_Address
    except:
        pass
    return None

def LDSP_Query(sock, IP_Broadcast, useFirst):
    if not hasattr(LDSP_Query, "txPacket"):
        # Construct the query packet
        header  = struct.pack("!6s", b'\x06LSDP\x01')
        message = struct.pack("!5s", b'\x05\x51\x01\x00\x01')
        LDSP_Query.txPacket = header + message
    # Send the packet and wait for response(s)
    sock.sendto(LDSP_Query.txPacket, (IP_Broadcast, 11430))
    timeout  = 0.750
    doneTime = time.time() + timeout
    while 1:
        try:
            sock.settimeout(timeout)
            rxPacket, address = sock.recvfrom(1024)
            IP_Address = LDSP_Add(rxPacket, address)
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

def GetBroadcastAddress():
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
    if not hasattr(LDSP_Query, "IP_Broadcast"):
        LDSP_Discovery.IP_Broadcast = GetBroadcastAddress()
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
    if not hasattr(SendGetRequest, "baseURL"):
        global IP_Device
        SendGetRequest.baseURL = "http://" + IP_Device + ":11000/"
    return requests.get(SendGetRequest.baseURL + request)

def VolumeUp(dB):
    SendGetRequest("Volume?db=" + dB)

def VolumeDown(dB):
    SendGetRequest("Volume?db=-" + dB)

def RefreshStatus():
    if not hasattr(RefreshStatus, "line"):
        RefreshStatus.line = "<Nothing playing>"
    status = SendGetRequest("Status")
    try:
        root   = vomit.fromstring(status.text)
        artist = root.find("artist").text
        song   = root.find("name").text
        RefreshStatus.line = artist + " : " + song
    except:
        pass
    stdscr.clear()
    stdscr.addstr(0, 0, RefreshStatus.line)
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
    global stdscr
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

if len(sys.argv) > 1:
    if sys.argv[1] == 'first':
        IP_Device = LDSP_Discovery(True)
    else:
        IP_Device = sys.argv[1]
else:
    IP_Device = LDSP_Discovery(False)

try:
    stdscr = ScreenInit()
    RefreshStatus()
    Loop()
except:
    pass

ScreenFini()
