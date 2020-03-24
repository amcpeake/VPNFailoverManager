import agent
import graphing

import subprocess
import json
import time
from datetime import datetime



def runCMD(cmd): # Run a command and return stdout as a string
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ps.communicate()[0].decode('utf-8')


# Script entry point

while True:
    print("Polling agent:")
    data = agent.poll(10)
    for i in data:
        i["time"] = str(datetime.now()) # Get time at the manager to account for transmission time

    print("Generating graph....", end="")
    with open('MIB.txt', 'w') as MIB:
        json.dump(data, MIB)
    graphing.genGraph("MIB.txt")
    print("done")

    print("Sleeping...")
    time.sleep(500)
