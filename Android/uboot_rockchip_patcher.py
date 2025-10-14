#!/usr/bin/python

import fdt
import sys
from hashlib import sha256

print("Output in: ./uboot_patched.img")

SZ = 0x200000
try:
    with open(sys.argv[1], 'rb') as f:
        img = f.read()
except IndexError as e:
    print("Usage: uboot_rockchip_patcher.py uboot_a.img")
    print("File missing")
    sys.exit(0)

assert img[SZ:] == img[:SZ]  # the uboot image contains the same data two times

replace_old = bytearray.fromhex("\
    FD 7B BE A9  FD 03 00 91  04 18 40 B9  F3 0B 00 F9 \
    81 00 01 8B  24 00 02 8B  9F 40 40 F1  49 01 00 54 \
    F3 03 02 AA  81 19 80 52  42 D8 77 D3  E0 03 03 AA ")

replace_new = bytearray.fromhex("\
    FD 7B BE A9  FD 03 00 91  04 18 40 B9  F3 0B 00 F9 \
    81 00 01 8B  24 00 02 8B  9F 40 40 F1  0A 00 00 14 \
    F3 03 02 AA  81 19 80 52  42 D8 77 D3  E0 03 03 AA ")

replace_offset = img.find(replace_old)
assert replace_offset > 0

dt = fdt.parse_dtb(img[:SZ])
ub = dt.get_node('images/uboot')
sz = ub.get_property('data-size').value
pos = ub.get_property('data-position').value
h = sha256(img[pos:pos + sz]).digest()
hash_offset = img.find(h)
assert hash_offset > 0

uboot_patched = bytearray(img)
uboot_patched[replace_offset:replace_offset + len(replace_new)] = replace_new
uboot_patched = uboot_patched[pos:pos + sz]

assert len(uboot_patched) == sz
h2 = sha256(uboot_patched).digest()

img2 = bytearray(img[:SZ])
img2[pos:pos + sz] = uboot_patched
img2[hash_offset:hash_offset + len(h)] = h2

with open('uboot_patched.img', 'wb') as f:
    f.write(img2)
    f.write(img2)
