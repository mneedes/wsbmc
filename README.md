
# World's Saddest BluOS(tm) (compatible) Media Controller

This is distributed under the Modified "shit-ware" license (see LICENSE.md).

## What? Why? How?

I wanted to control my BluOS device(s) in Linux from a small window (BluOS doesn't support Linux and their UI isn't small). This implementation is written in python and uses a dirt-simple curses interface. It makes use of BluOS' remote integration API. It seems to work pretty well for what it is...

Feature Summary:

- Simple commands (forward, skip, volume up/down, mute, pause)
- Artist/song display
- Small window UI
- Auto-discovery (Work In Progress)

## Prerequisitez

- Python 3.10 or better (I refused to use python until they implemented a switch/case equivalent, and I waited a LONG time)
- You need "requests" and "netifaces" so invoke 'pip3 install requests netifaces' if you don't have them!
- For auto-discovery to work you will need to allow UDP port 11430 broadcasts through your firewall,
    If it doesn't work, try the following command: "sudo ufw allow 11430/udp"
    - Auto-discovery is optional if you already know the IP address of your BluOS device.

## Instructionz

1. Open a terminal and invoke (NOTE: This is WIP and doesn't work exactly yet, so use the other options):
   > `python3 ./wsbmc.py`
2. Or, if you only have one BluOS device, invoke the following and it will connect to the first BluOS device it finds! Also great if you like to gamble.
   > `python3 ./wsbmc.py first`
3. Or, if you already know the IP address of the BluOS device, use the following, where IPADDR is your device's IP (e.g.: 192.168.1.110).
   > `python3 ./wsbmc.py IPADDR`
4. The following key commands are supported by the player:

> u - volume up (and unmute)
> d - volume down
> m - mute
> p - toggle pause
> s - skip track
> b - back track
> q - quit WSBMC
> r - refresh display

## Notez

1. The API used by WSBMC may be found here:
     https://bluos.io/wp-content/uploads/2023/09/BluOS-Custom-Integration-API-v1.5.pdf

