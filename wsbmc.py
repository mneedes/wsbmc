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
# Wow, finally some good names, thank goodness at least someone has some sense.
import sys, time, random, struct, socket, ipaddress

IP_Broadcast="192.168.1.255"
IP_Device="192.168.1.100"

def get_subnet_mask(ip_address_with_prefix):
    """
    Extracts the subnet mask from an IP address string that includes a prefix length (CIDR notation).

    Args:
        ip_address_with_prefix: IP address and prefix length (e.g., "192.168.1.1/24").

    Returns:
        The subnet mask as a string (e.g., "255.255.255.0").
        Returns None if the input is invalid.
    """
    try:
        network = ipaddress.ip_network(ip_address_with_prefix, strict=False)
        return str(network.netmask)
    except ValueError:
        return None

# Example usage
ip_address_with_prefix = "192.168.1.1/24"
subnet_mask = get_subnet_mask(ip_address_with_prefix)

if subnet_mask:
    print(f"The subnet mask for {ip_address_with_prefix} is: {subnet_mask}")
else:
    print(f"Invalid IP address or format: {ip_address_with_prefix}")

def GetBroadcastAddress():
    network = ipaddress.ip_interface(f"{ip_address}/{subnet_mask}")
    return str(network.network.broadcast_address)

def LDSP_Add(data, addr):
    None
    # print(data)
    # print(addr)

print(socket.gethostbyname(''))

def LDSP_Query(sock):
    if not hasattr(LDSP_Query, "packet"):
        # Construct the query packet
        header  = struct.pack("!6s", b'\x06LSDP\x01')
        message = struct.pack("!5s", b'\x05\x51\x01\x00\x01')
        LDSP_Query.packet = header + message
    # Send the packet and wait up to 750ms for response(s)
    sock.sendto(LDSP_Query.packet, (IP_Broadcast, 11430))
    timeout  = 0.750
    doneTime = time.time() + timeout
    while 1:
        try:
            sock.settimeout(timeout)
            data, addr = sock.recvfrom(1024)
            LDSP_Add(data, addr)
        except socket.timeout:
            None
        except socket.error as e:
            print(f"Socket error: {e}")
            break
        timeout = doneTime - time.time()
        if timeout < 0:
            break

def LDSP_Discovery():
    # Set up a UDP broadcast socket
    sock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP_Broadcast, 11430))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Fire off the seven (Sieben, (Siete (6+1))) query packets
    #   and obtain response(s)
    fireTimes = [ 1, 2, 3, 5, 7, 10 ]
    startTime = time.time()
    #TODO:
    #for p in range(6):
    for p in range(3):
        LDSP_Query(sock)
        waitTime  = fireTimes[p] - (time.time() - startTime)
        waitTime += 0.001 * random.randint(0, 250)
        if waitTime > 0:
            time.sleep(waitTime)
    LDSP_Query(sock)
    sock.close()
    # TODO: Determine actual IP
    return IP_Device

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

if len(sys.argv) > 1:
    IP_Device = sys.argv[1]
else:
    IP_Device = LDSP_Discovery()

baseURL="http://" + IP_Device + ":11000/"
stdscr = ScreenInit()

try:
    #stdscr = ScreenInit()
    RefreshStatus()
    Loop()
except:
    None

ScreenFini()

