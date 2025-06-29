# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()


#####
#####
##### reset counter an nvs control
import esp32
import os

def nvssave( key, val ):
    #esp32.NVS("memory").erase_key( key )
    esp32.NVS("memory").set_blob( key, str( val ).encode() )
    esp32.NVS("memory").commit()
    return

def nvsload( key ):
    nvsbuffer = bytearray( 50 )
    nvsbufferlen = esp32.NVS( "memory" ).get_blob( key, nvsbuffer )
    return nvsbuffer[ 0:nvsbufferlen ].decode()

def nvsdel( key ):
    esp32.NVS("memory").erase_key( key )
    return

#####
#####
#####
try:
    resetcnt = nvsload( "cnt" )
    resetcnt = int(resetcnt) + 1
    nvssave( "cnt", resetcnt )
    if resetcnt > 6:
        file = open('reset.txt', 'wt')
        file.write("reseted with power button !!!")
        file.close()
        try:
            os.remove('wlan.txt')
        except:
            pass
        try:
            os.remove('domains.txt')
        except:
            pass
except:
    nvssave( "cnt", 1 )

#####
#####
#####
def urlencode(params):
    def to_hex(byte):
        hex_chars = "0123456789ABCDEF"
        return "%" + hex_chars[byte >> 4] + hex_chars[byte & 0x0F]

    def quote(s):
        safe = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~"
        result = b""
        for c in s:
            if c in safe:
                result += bytes([c])
            else:
                result += to_hex(c).encode()
        return result

    encoded = []
    for key, value in params.items():
        k = quote(str(key).encode('utf-8'))
        v = quote(str(value).encode('utf-8'))
        encoded.append(k + b"=" + v)
    return b"&".join(encoded).decode()

#####
def urldecode( query ):
    if query == "":
        return {}
    #
    def from_hex(hexstr):
        return int(hexstr[0], 16) * 16 + int(hexstr[1], 16)
    #
    def unquote(s):
        result = bytearray()
        i = 0
        while i < len(s):
            c = s[i]
            if c == '%':
                byte = from_hex(s[i+1:i+3])
                result.append(byte)
                i += 3
            elif c == '+':
                result.append(ord(' '))
                i += 1
            else:
                result.append(ord(c))
                i += 1
        return result.decode('utf-8')
    #
    pairs = query.split('&')
    result = {}
    #
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            key, value = pair, ''
        result[unquote(key)] = unquote(value)
    #
    return result
