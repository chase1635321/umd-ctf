#!/usr/bin/python3

import r2pipe
import sys
import os
import string

arr = []

def attempt(stdin):
    with open("profile.rr2", "w+") as f:
        f.write('#!/usr/bin/rarun2\nprogram=hashmenot\nstdin=\"' + stdin + '\"\n')

    r = r2pipe.open("hashmenot")
    r.cmd("e dbg.profile=profile.rr2")

    r.cmd("ood")
    r.cmd("dcu 0x4009fd")
    #print(" > " + c + " -> " + r.cmd("ps @ rdi"))
    arr.append((stdin, r.cmd("ps @ rdi").strip()))
    r.cmd("doc")

def main():
    global arr
    for c in list(string.printable):
        attempt(c)
    print("="*20 + " Done " + "="*20)
    for a, b in arr:
        print(" > " + a + " -> " + b)

    s = "b9850b343b9e936db9850b34c5d42e20431b4157975467aee4d47935b3d7255a31ccbd038438fff8c483ccef80ec08d64cca7ad8eb0542ba"
    n = 8
    chunks = [s[i:i+n] for i in range(0, len(s), n)]
    print(chunks)
    print("")

    for chunk in chunks:
        temp = "?"
        for x, y in arr:
            if y.strip() == chunk.strip():
                temp = x.strip()
        print(temp, end='')

main()
