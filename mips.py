#! /usr/bin/env python2

import angr
import struct

p = angr.Project("mips")
f = angr.claripy.BVS("pw", 4 * 8)
st = p.factory.path(args=["./mips", f])
pg = p.factory.path_group(st)

pg.explore(find=0x4004d6, avoid=0x4004ca)

for found in pg.found:
    out = ''
    pw = found.state.se.any_str(f)
    x, = struct.unpack("<I", pw)
    print pw.encode("hex")
    print hex(x)
