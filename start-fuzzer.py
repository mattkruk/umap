#!/usr/bin/python3

import re
import subprocess
import sys

def get_supported_drivers(node):
    outp = subprocess.check_output(["./umap.py", "-P", node, "-i"])
    return(re.findall(r"([0-9a-fA-F]+):([0-9a-fA-F]+):([0-9a-fA-F]+).*?\*\*SUPPORTED\*\*", str(outp), re.DOTALL))

def fuzz_driver(node, driver):
    print("Fuzzing %s" % (driver, ))
    outp = subprocess.check_output(["./umap.py", "-P", node, "-f", "%s:A" % (driver, )])
    return(outp)

if len(sys.argv) < 2:
    print("Usage: %s device" % (sys.argv[0], ))
    sys.exit(1)

drivers = get_supported_drivers(sys.argv[1])
for driver in drivers:
    drvstr = "%s:%s:%s" % driver
    r = fuzz_driver(sys.argv[1], drvstr)
    fd = open("./fuzz_%s" % (drvstr, ), "w+")
    fd.write(str(r).replace("\\n", "\n"))
    fd.close()
sys.exit(0)
