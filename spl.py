#! /usr/bin/env python2

from subprocess import Popen, PIPE, STDOUT
import string
from pwn import *

end = "tu1|\h+&g\OP7@% :BH7M6m3g="
inp = "t"

while len(inp) != len(end):
    found = False

    for c in string.printable:
        tst = c + inp
        p = Popen("./asdf", stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        res = p.communicate(input=tst + " ")[0]
        # p = process("./asdf")
        # p.send(tst + " ")
        # res = p.recvall()

        if res == end[:len(tst)]:
            print "found: " + c + inp
            inp = c + inp
            found = True
            break

    if not found:
        print "oops"
        break
