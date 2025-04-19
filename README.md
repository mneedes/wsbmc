
# World's Saddest BluOS(tm) (compatible) Media Controller

This is distributed under the Modified "shit-ware" license (see LICENSE.md).

## What? Why? How?

I want to control my BluOS device(s) from a small Linux terminal window. This implementation is written in python and uses a dirt-simple curses interface. It makes use of BluOS' remote integration API. You need a keyboard to use this (shocking I know).

Feature Summary:

- Simple commands (skip, back, volume up/down, mute, pause)
- Artist/song display (may not work in all applications, not my fault)
- Small window UI
- Auto-discovery

## Prerequisitez

- Python 3.10 or better (I refused to use python until they implemented a switch/case equivalent, and I waited a LONG time)
- You need python's "requests" and "netifaces" so try the following if you don't have them:
  ```
  pip3 install requests netifaces
  ```
- For auto-discovery to work (OPTIONAL(\*)) you will need to allow UDP port 11430 broadcasts through your firewall.
    If auto-discovery isn't working, try the following:
  ```
  sudo ufw allow 11430/udp
  ```
    - (\*) Auto-discovery is optional if you already know the IP address of your BluOS device (and your router is well behaved).

## Instructionz

1. Open a terminal and invoke (this does a "deep" scan):
   ```
   python3 ./wsbmc.py
   ```
3. Or, if you only have one BluOS device, invoke the following and it will connect to the first BluOS device it finds! Also great if you have *more* than one BluOS device and you like to gamble.
   ```
   python3 ./wsbmc.py first
   ```
5. Or, if you already know the IP address of the BluOS device (IP\_ADDRESS is your device's IP, *e.g.:* 192.168.1.110):
   ```
   python3 ./wsbmc.py IP_ADDRESS
   ```
6. The following key-press commands are supported by the controller:

```
 u - volume up (and unmute)
 d - volume down
 m - mute
 p - toggle pause
 s - skip track
 b - back track
 q - quit WSBMC
```

## Notez / Known Issues

1. The artist/song display doesn't work with Radio Paradise and possibly other apps.
    + This is likely a BluOS limitation since Status Requests are returning `<Response [200]>` when I run Radio Paradise.
2. The API used by WSBMC may be found here:
     https://bluos.io/wp-content/uploads/2023/09/BluOS-Custom-Integration-API-v1.5.pdf

