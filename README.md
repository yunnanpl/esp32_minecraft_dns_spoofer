# Minecraft Bedrock DNS spoofer ESP32
A DNS spoofer based on ESP32 to play on custom servers on Console Minecraft Bedrock.

# Problem
It is widely known, that on console Minecraft Bedrock, the choice of servers is fixed and limited (~6 predefined servers).
There is no easy possiblity to connect to private or custom servers.

This is clearly very strange, as such stand-alone dedicated servers are provided... but those work only with PC version of Minecraft Bedrock, which can connect to any server with host name or IP.

# Problem, level 2
Strangely, such dedicated Minecraft Bedrock server is hardly usable even in local network !!!
Commonly, it does not appear in the list at all.
So, not even a solution to "escape" the server limitation is necessary, but also for a normal game functionality.

# Possibilities
Now, there are multiple methods, allowing to go around this.
= user has to be invited to the custom server by a PC player
= user has to use public DNS spoofers, and then in the game, type the IP address of the requested server

# Solution
The above solutions are fine, but maybe something more local and safe can be built ?
So, using and DNS functionality on ESP32 with Micropython, it is possible to spoof some DNS adresses, thus substituting the official list of servers, with custom or local ones !





