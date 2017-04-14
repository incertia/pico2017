#!/usr/bin/env python2
import random,string

flag = ""
encflag = "BNZQ:1l36de9583w5516fv3b8691102224f3e"
random.seed("random")
for c in encflag:
  if c.islower():
    #rotate number around alphabet a random amount
    flag += chr((ord(c)-ord('a')-random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    flag += chr((ord(c)-ord('A')-random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
    flag += chr((ord(c)-ord('0')-random.randrange(0,10))%10 + ord('0'))
  else:
    flag += c
print "Unguessably Randomized Flag: "+flag
