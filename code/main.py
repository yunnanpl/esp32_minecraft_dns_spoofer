
##### micropython minecraft server spoofer v2

import network
from microDNSSrv import MicroDNSSrv
import machine
import socket
import time
import binascii
import os
import gc
gc.enable()

#####
#####
#####

def info( *valInfo ):
    #val = list( val )
    #for nnn, zzz in enumerate( val ):
    #    try:
    #        val[nnn] = zzz.decode()
    #    except:
    #        val[nnn] = str( zzz )
    #    #print( zzz )
    print( valInfo )
    #print( str( " ".join( val ) ) )
    return

#####
#####
#####
# change clock
#machine.freq(240000000)

wlan = network.WLAN( network.STA_IF )
wlan.active( False )

wlanAP = network.WLAN( network.AP_IF )
wlanAP.active( False )

#####
#####
##### try normal network
wlanData = []
wlanScan = []
wlanType = ""
try:
    #####
    file = open('wlan.txt','rt') # if file not exist then 
    wlanData = file.read()
    file.close()
    wlanData = eval( wlanData )
    #####
    wlan.active( True )
    wlan.connect( wlanData[0], binascii.unhexlify( wlanData[1] ) ) # this has to be after true
    #####
    for _ in range(5):
        time.sleep(1)
        if wlan.isconnected():
            wlanAP.active( False )
            #print("+++ Network started. IP:", str( wlan.ifconfig()[0] ), "host: mcspoof")
            info( "+++ Network started. IP:", str( wlan.ifconfig()[0] ), "host: mcspoof" )
            wlanType = "STA"
            break
    else:
        raise Exception('no wifi connection')
    #sys.exit()
    #####
except Exception as e:
    ##### if any problem with connection, open AP
    wlan.active( False )
    wlan.active( True )
    wlanScan = wlan.scan()
    wlanAP.active( True )
    wlanAP.config( essid="MCSPOOF" )
    #print("--- AP started.", str( wlanAP.ifconfig()[0] ), "essid: MCSPOOF")
    info("--- AP started.", str( wlanAP.ifconfig()[0] ), "essid: MCSPOOF")
    wlanType = "AP"
    #pass
    #####

network.hostname('mcspoof')

#####
#####
#####
#if wlan.isconnected() == True and wlanAP.isconnected() == False:
#if wlan.ifconfig()[0] != "0.0.0.0" and wlanAP.ifconfig()[0] == "0.0.0.0":
domainsName = {
    "*inpvp.net"           : "Mineville",   # mineville
    "*lbsg.net"            : "Lifeboat",   # lifeboat
    "*cubecraft.net"       : "CubeCraft",   # cubecraft
    "*hivebedrock.network" : "The Hive",   # hive
    "*galaxite.net"        : "Galaxite",    # galaxite
    "*enchanted.gg"        : "enchanted dragons",
    #"*mineplex.com"        : "Mineplex ?",   # mineplex
    #"*pixelparadise.gg"    : "Pixel Paradise ?",   # pixel paradise
    "*gstatic.com"         : "CAPTIVE",
}
#####
if wlanType == "STA":
    try:
        #####
        file = open('domains.txt', 'rt')
        domainsListRAW = file.read()
        domainsList = eval( domainsListRAW )
    except:
        #####
        domainsList = {
            "*inpvp.net"           : "empty",   # mineville
            "*lbsg.net"            : "empty",   # lifeboat
            "*cubecraft.net"       : "empty",   # cubecraft
            "*hivebedrock.network" : "empty",   # hive
            "*galaxite.net"        : "empty",   # galaxite
            "*enchanted.gg"        : "empty",   # enchanted dragons
            #"*gstatic.com"         : "192.168.4.1",
            #"*mineplex.com"        : "192.168.1.7",   # mineplex
            #"*pixelparadise.gg"    : "192.168.1.8",   # pixel paradise
        }
        #####
else:
    #####
    domainsList = {
        "*gstatic.com"         : "192.168.4.1",
    }

#####
#####
#####
mds = MicroDNSSrv()
mds.SetDomainsList( domainsList )
#mds.Create( domainsList )
if mds.Start() :
    info("+++ MicroDNSSrv started.")
else :
    info("--- MicroDNSSrv error, not started.")
#####
#####
#####


#####
#####
#####
def header( type, len=0, loc="/" ):
    if str( type ) == "302":
        headerTxt = b"""HTTP/1.1 302 Found
Location: """ + str( loc ) + """
Connection: close
"""
    # Content-Length: """ + str( len ) + """
    elif str( type ) == "404":
        headerTxt = b"""HTTP/1.0 404 Not Found
Connection: close
"""
    elif str( type ) == "200plain":
        headerTxt = b"""HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: """ + str( len ) + """

"""
    elif str( type ) == "200html":
        headerTxt = b"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: """ + str( len ) + """

"""
    elif str( type ) == "200json":
        headerTxt = b"""HTTP/1.1 200 OK
Content-Type: application/captive+json"""
    return headerTxt

#####
#####
#####
pageHead = '''<html>
<head>
<title>ESP32_MC_DNS_spoofer</title>
<style>
html {
 zoom: 1.4;
 background-color: #fff
}
body {
 display: block;
 width: 500px;
 background-color: #eee;
 font-size: 120%;
 padding: 10px;
}
td > p, input, select {
 font-size: 120%;
 font-weight: bold;
}
input#ip {
 width: 180px;
}
</style>
<!-- meta -->
</head>
<body>
<h2>ESP32_MC_DNS_spoofer</h2>
By Dr.JJ 2025<br/>
Minecraft Bedrock DNS spoofer to play on arbitrary custom servers, running on ESP32.<br/>
<a href="">Seite neu laden</a><br/>
<a href="/reset">Chip neustarten</a><br/>
<a href="/remove">Vom Netzwerk trennen</a><br/>
'''

#####
#####
#####
def webPage():
    domainPage = ""
    for www in domainsList.items():
        if mds._domList.get( www[0] ) == None:
            theStyle = 'style="background-color:#F99"'
        else:
            theStyle = 'style="background-color:#9F9"'
        domainPage += '<form action="/setDomain"><tr><td><input type="hidden" id="domain" name="domain" value="' + www[0] + '"><p>' + domainsName.get( www[0] ) + '</p></td>\n<td><input type="text" id="ip" name="ip" value="' + www[1] + '" ' + theStyle + '><input type="submit" value="SET" /></td></tr></form>\n'
    pageOut = pageHead
    pageOut += '''<h3>Info</h3>
Neue DNS Server addresse.<br/>
So in Nintendo einstellen.<br/>
''' + str( wlan.ifconfig()[0] ) + '''<br/>
1.1.1.1

<br/>
<h3>Minecraft Server ersetzen</h3>
<table>
''' + domainPage + '''
</table>
</body>
</html>'''
    return pageOut.encode()

#####
#####
#####
def webAPPage():
    #return pageOut.encode()
    #wlanScan
    wlanScanUniq = list( set( [ aaa[0].decode() for aaa in wlanScan ] ) )
    wlanOptList = "".join( [ '<option value="'+aaa+'">'+aaa+"</option>\n" for aaa in wlanScanUniq ] )
    #
    pageOut = pageHead
    pageOut += '''<h3>WLAN Verbindung</h3>
<form action="/setWlan" method="post">
WLAN:<br/>
<select id="theWlan" name="theWlan">
''' + wlanOptList + '''<br/>
</select><br/>
Passwort:<br/>
<input type="password" id="thePass" name="thePass" /><br/>
<input type="submit" value="SET WLAN" />
</form>

</body>
</html>'''
    return pageOut.encode()

#####
#####
#####
def webAPRefresh( theUrl="" ):
    if theUrl != "":
        pageOut = pageHead.replace('<!-- meta -->', '<meta http-equiv="refresh" content="2; url='+ theUrl +'">')
    else:
        if str( wlan.ifconfig()[0] ) == '0.0.0.0':
            pageOut = pageHead.replace('<!-- meta -->', '<meta http-equiv="refresh" content="2">')
        else:
            pageOut = pageHead.replace('<!-- meta -->', '<meta http-equiv="refresh" content="2, url=\'/generate_204\'">')
            #pageOut = pageHead.replace('<!-- meta -->', '<meta http-equiv="refresh" content="2, url=\'http://192.168.1.102\'">')
    #
    pageOut += '''<h3>Bitte warten !!!</h3>
Verbinde zum WLAN...
</body>
</html>'''
    return pageOut.encode()

def webAPConn():
    pageOut = pageHead
    if str( wlan.ifconfig()[0] ) == '0.0.0.0':
        pageWlan = "Nicht verbunden."
    else:
        pageWlan = "Verbunden !!!<br>Neue addresse "+ str( wlan.ifconfig()[0] ) + "."
        file = open('wlan.txt','wt')
        file.write( str( [ wlanData[0], binascii.hexlify( wlanData[1] ).decode() ] ) )
        file.close()
        info( 'Wlan saved' )
        pageOut = pageHead.replace('<!-- meta -->', '<meta http-equiv="refresh" content="25, url=\'/reset\'">')
        #wlanAP.active( False )
        #wlanAP.disconnect()
    pageOut += '''<h2>Success</h2>
<h3>Bitte neue addresse kopieren / speichern<h3>
<input type="text" value="http://''' + str( wlan.ifconfig()[0] ) + '''/" id="ipField" readonly onclick="this.select();"><br/>
<p>Neustart in <span id="counter"></span> Sekunden.<p>
</form>
<script>
var downTime = 15;
var x = setInterval( function() {
	downTime = downTime - 1;
	if ( downTime < 0 ) {
		downTimeText = "rebooting";
	} else {
		downTimeText = downTime;
	}
	document.getElementById("counter").innerHTML = downTimeText;
}, 1500 )
</script>
</body>
</html>'''
    return pageOut.encode()

#<a href="http://''' + str( wlan.ifconfig()[0] ) + '''/" target="_blank">Click here to continue</a><br/>
#<input type="button" onclick="navigator.clipboard.writeText(\'http://''' + str( wlan.ifconfig()[0] ) + '''/\')" value="Link kopieren" /><br/>
#<a href=intent://''' + str( wlan.ifconfig()[0] ) + '''/#Intent;scheme=http;end">intent</a>
#<form action="/restart">
#<input type="submit" value="Restart" />

# <a href=//"''' + str( wlan.ifconfig()[0] ) + '''/"><a/>
#####
#####
#####
def req_handler( cs ):
    ### this function knows about the request
    global domainsList
    global mds
    global wlanData
    #global machine
    try:
        #####
        req = cs.read().decode("utf-8")
        #print( req )
        if ( req.split("\r\n") )[0].strip() == "":
            #info( '=0=', req )
            #cs.write( header("302") )
            #time.sleep(1)
            cs.close()
            return
        host = ( req.split("\r\n") )[1].strip().split(": ")[1].strip()
        #print( host )
        uri = ( req.split("\r\n") )[0].strip().split(" ")[1].strip().replace('%20', ' ')
        valVar = ""
        theType = req[0:3]
        #####
        #####
        #####
        if uri == '/favicon.ico':
            #pass
            #header404
            cs.write( header("404") )
            cs.close()
            return
        #####
        #####
        #####
        if theType == "POS":
            valVar = req.split('\r\n\r\n')[-1]
            #####
        elif theType == "GET":
            if len( uri.split('?') ) > 1:
                valVar = uri.split('?')[-1]
                uri = uri.split('?')[0]
            else:
                valVar = ""
        else:
            valVar = ""
        #####
        #####
        #####
        if req:
            #info( 'req:', uri, theType, valVar )
            #####
            ##### web for AP, captive
            #####
            if uri == '/reset':
                info( 'resetting' )
                cs.write( header("302") )
                cs.close()
                machine.reset()
                try:
                    wlanAP.disconnect()
                except:
                    pass
                try:
                    wlan.disconnect()
                except:
                    pass
                #time.sleep( 0.2 )
                #time.sleep( 1 )               
            #####
            elif uri == '/remove':
                info( 'remove settings' )
                #import os
                #try:
                #    os.remove('domains.txt')
                #except:
                #    pass
                try:
                    os.remove('wlan.txt')
                except:
                    pass
                cs.write( header("302") )
                cs.close()
                #time.sleep( 0.2 )
                machine.reset()
                #time.sleep(0.1)
            #####
            #####
            #####
            if wlanAP.active() == True and wlanAP.ifconfig()[0] != "0.0.0.0" and host != wlan.ifconfig()[0]: # and wlan.co:
                #print( 'ap', uri, valVar )
                ##### captive
                if uri == '/generate_204':
                    if wlan.ifconfig()[0] == "0.0.0.0":
                        webPageTxt = webAPPage()
                        cs.write( header("200html", len(webPageTxt) ) + webPageTxt )
                    else:
                        webPageTxt = webAPConn()
                        cs.write( header("200html", len(webPageTxt) ) + webPageTxt )
                        #time.sleep( 30 )
                        #wlanAP.disconnect()
                        #wlanAP.active( False )
                        #machine.reset()
                    #else:
                    #    cs.write( header( "302", 0, loc="http://" + wlan.ifconfig()[0] + "/" ) )
                    #time.sleep( 1 )
                    #cs.close()
                ##### set wlan
                if uri == '/setWlan':
                    #####
                    wlanDataUrl = urldecode( valVar )
                    #print( wlanDataUrl )                   
                    if len( wlanDataUrl ) == 2:
                        try:
                            #wlan = network.WLAN( network.STA_IF )
                            wlanData = [ wlanDataUrl['theWlan'], wlanDataUrl['thePass'] ]
                            wlan.connect( wlanData[0], wlanData[1] )
                            time.sleep(0.2)
                            wlan.connect()
                            time.sleep(0.2)
                            cs.write( header( "302", 0, "/setWait" ) )
                        except Exception as e:
                            info( e )
                            #cs.write( header( "302" ) )
                            cs.write( header( "302", 0, "/setWait" ) )
                            pass
                    else:
                        cs.write( header( "302", 0, '/generate_204' ) )
                    #webPageTxt = webRefresh()
                    #cs.write( header("200html", len(webPageTxt) ) + webPageTxt )
                elif uri == '/setWait': # and wlan.:
                    #if wlan.isconnected() == True and str( wlan.ifconfig()[0] ) != "0.0.0.0":
                    #    #redirurl
                    #    cs.write( header( "302", 0, loc="/generate_204" ) )
                    #    #webPageTxt = webAPRefresh( "http://" + str(wlan.ifconfig()[0]) + "/" )
                    #    #cs.write( header("200html", len(webPageTxt) ) + webPageTxt )
                    #else:
                    webPageTxt = webAPRefresh()
                    cs.write( header("200html", len(webPageTxt) ) + webPageTxt )
                    #cs.close()
                else:
                    ##### normal page
                    #if str( wlan.ifconfig()[0] ) == "0.0.0.0":
                    cs.write( header( "302", 0, loc="/generate_204" ) )
                    #elif str( wlan.ifconfig()[0] ) != "0.0.0.0":
                    #    cs.write( header( "302", 0, loc="/generate_204" ) )
                    #    #time.sleep(1)
                    #    #wlanAP.active( False )
                    #    #time.sleep(3)
            #####
            else:
                #####
                #info( 'wlan', uri, valVar )
                #####
                if uri == "/setDomain":
                    #
                    newDomain = valVar.split('&')[0].split('=')[1].strip()
                    newIp = valVar.split('&')[1].split('=')[1].strip()
                    #print( newDomain, newIp )
                    domainsList[ newDomain ] = newIp
                    #print( domainsList )
                    mds.SetDomainsList( domainsList )
                    #
                    file = open('domains.txt', 'wt')
                    file.write( str( domainsList ) )
                    file.close()
                    #
                    #time.sleep(0.1)
                    cs.write( header("302") )
                    #time.sleep(0.1)
                #####
                else:
                    ##### normal page
                    if wlanAP.active() == True:
                        webPageTxt = webAPRefresh("/")
                        cs.write( header("200html", len(webPageTxt) ) + webPageTxt )
                    else:
                        webPageTxt = webPage()
                        cs.write( header("200html", len(webPageTxt) ) + webPageTxt )
        #####
        else:
            #print( 'Client close connection' )
            cs.write( header404 )
            #pass
    except Exception as e:
        #pass
        info( 'Err req_handler:', e )
    #signalLed.off()
    cs.close()

def cln_handler( srv ):
    ### this function knows about the client
    cs, ca = srv.accept()
    #print( 'Serving:', ca )
    #print( srv.readline() )
    cs.setblocking( False )
    cs.setsockopt( socket.SOL_SOCKET, 20, req_handler )

#####
##### web server
#####
port = 80
addr = socket.getaddrinfo( wlan.ifconfig()[0], port )[0][-1]

srv = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
srv.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

srv.bind( addr )
srv.listen( 3 ) # at most 5 clients
srv.setblocking( False )
srv.setsockopt( socket.SOL_SOCKET, 20, cln_handler )

info("+++ WebSrv started.")

#####
#####
#####
nvsdel( "cnt" )

#####
#####
#####


