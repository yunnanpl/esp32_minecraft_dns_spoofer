# Minecraft Bedrock DNS spoofer ESP32
A DNS spoofer based on ESP32 to play on custom servers on Console Minecraft Bedrock.

## Problem
It is widely known, that on console Minecraft Bedrock, the choice of servers is fixed and limited (~6 predefined servers).

There is no easy possiblity to connect to private or custom servers.

This is clearly very strange, as such stand-alone dedicated servers are provided... but those work only with PC version of Minecraft Bedrock, which can connect to any server with host name or IP.

## Problem, level 2
Strangely, such dedicated Minecraft Bedrock server is hardly usable even in local network !!!

Commonly, it does not appear in the list at all.

So, not even a solution to "escape" the server limitation is necessary, but also for a normal expected in-game functionality.

## Possibilities
Now, there are multiple methods, allowing to go around this.

* user has to be invited to the custom server by a PC player
* user has to use public DNS spoofers, and then in the game, type the IP address of the requested server
* user can connect to a local server directly... this never works ;)

# Solution
The above solutions are fine, but maybe something more local and safe can be built ?
So, using and DNS functionality on ESP32 with Micropython, it is possible to spoof some DNS adresses, thus substituting the official list of servers, with custom or local ones !

## Requirements
In order to use it, one needs:
* EPS32 chip in nearly any type or shape will work, maybe even ESP8266 with micropython would work, but not sure about the webpage
* micropython binaries to flash
* code !!!
* local WLAN, to which the DNS spoofer can connect (at best with fixed local IP)

# Other
## Alternatives and history
* spoofing local LAN broadcast messages
In the past, it was partially possible to spoof a local LAN broadcast message, which consisted IP address and PORT of the custom server.
By doing so, one could connect to any server.

* spoofing local LAN broadcast messages in a virtual network
Later, this possiblity was limited, as no IP address was present in the packet, and only local addresses could broadcast messages.
Still, there was a possiblity to create Virtual LAN, and still use it

* now, the newer versions seem to use RakNet protocol... so it is not clear to me if there is a way to spoof it

# Requirements and references
Uses slightly changed MicroDNSSrv project:
 * https://github.com/jczic/MicroDNSSrv

## Other sources
* Minecraft detector and faker
  * https://github.com/ksaidev/Minecraft-Detector

* ESP32 S3 mini case from Thingverse
  *  https://www.thingiverse.com/thing:6841853
  * I printed it in semi-transparent to add some signal LEDs

* LANBroadcaster
  * This did not work... but sounds promising
  * https://github.com/bhopahk/LANBroadcaster
  * https://github.com/4drian3d/LANBroadcaster


