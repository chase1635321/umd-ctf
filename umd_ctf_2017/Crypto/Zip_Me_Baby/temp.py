#!/usr/bin/python

# zipeinfo - ZIP encryption info
# parses ZIP files and tells user about used encryption method

# created by Hanno Boeck, http://hboeck.de
# License: CC0 / Public Domain

from __future__ import print_function
import struct,optparse,sys

parser = optparse.OptionParser(usage="%prog [file(s)]")
(options, args) = parser.parse_args()
if len(args)==0:
    print("No arguments given!")
    parser.print_help()
    sys.exit(1)

for zipfile in args:
    print ("* %s" % zipfile)
    f = open(zipfile,"rb")

    pos=0
    iszip=0
    while 1:
        head=f.read(4)
        if head != b"PK\x03\x04": break
        iszip=1
        version=struct.unpack("H", f.read(2))[0]
        bitfield=struct.unpack("H", f.read(2))[0]
        enc=bitfield&1
        ses=(bitfield&(1<<6))>>6
        comp=struct.unpack("H", f.read(2))[0]
        f.seek(pos+0x12)
        data_len=struct.unpack("I", f.read(4))[0]
        f.seek(pos+0x1a)
        name_len=struct.unpack("H", f.read(2))[0]
        extra_len=struct.unpack("H", f.read(2))[0]
        filename=f.read(name_len).decode("ascii")
        print("-> %s " % filename.ljust(12), end="")
    
        if enc==0: print("not encrypted  [-]")
        elif comp==99: # WinZip AES
            f.seek(pos+0x1e+name_len)
            headid=struct.unpack("H", f.read(2))[0]
            f.seek(pos+0x1e+name_len+4)
            aesver=struct.unpack("B", f.read(1))[0]
            f.seek(pos+0x1e+name_len+8)
            aessize=struct.unpack("B", f.read(1))[0]
            if headid!=0x9901 or (aesver!=1 and aesver!=2): print("WinZip/error   [ok]")
            elif aessize==1: print("WinZip/AES128v%i[ok]" % aesver)
            elif aessize==2: print("WinZip/AES192v%i[ok]" % aesver)
            elif aessize==3: print("WinZip/AES256v%i[ok]" % aesver)
            else: print("WinZip/unknown [?]")

        elif ses==1: # PKWARE Strong Encryption Specification
            f.seek(pos+0x1e+name_len)
            ivsize=struct.unpack("H", f.read(2))[0]
            f.seek(pos+0x1e+name_len+ivsize+8)
            algid=struct.unpack("H", f.read(2))[0]
            if algid==0x6601: print("PKZIP/DES      [insecure]")
            elif algid==0x6602: print("PKZIP/RC2old   [insecure]")
            elif algid==0x6603: print("PKZIP/3DES168  [ok]")
            elif algid==0x6609: print("PKZIP/3DES112  [weak]")
            elif algid==0x660E: print("PKZIP/AES128   [ok]")
            elif algid==0x660F: print("PKZIP/AES192   [ok]")
            elif algid==0x6610: print("PKZIP/AES256   [ok]")
            elif algid==0x6702: print("PKZIP/RC2new   [insecure]")
            elif algid==0x6720: print("PKZIP/Blowfish [ok]")
            elif algid==0x6721: print("PKZIP/Twofish  [ok]")
            elif algid==0x6801: print("PKZIP/RC4      [weak]")
            else: print("PKZIP/unknown   [?]")
        else: print("PKZIP/legacy   [insecure]")
        pos+=0x1e+name_len+extra_len+data_len
        f.seek(pos)
    if iszip==0: print("-> ERROR: No ZIP")
    f.close()
