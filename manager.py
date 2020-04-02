import agent
from syncStore import Store
import graphing

import subprocess
import time


def runCMD(cmd): # Run a command and return stdout as a string
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ps.communicate()[0].decode('utf-8')


def pickTun(data, config):
    scores = {}
    active = runCMD("./scripts/switchTuns.sh active | grep -oE 'tun[0-9]+'").strip("\n")
    for tun in data:
        if len(data[tun]) < config["depth"]: # We don't have enough measurements for this int to make a decision
            continue

        measurements = data[tun][:config["depth"]] # Depth defines how many measurements to use
        score = 0
        for measure in measurements: # Higher score is better
            score += measure["upload"] * config["uploadWeight"]
            score += measure["download"] * config["downloadWeight"]
            score += (1 / measure["latency"]) * config["latencyWeight"] # Lower latency is better hence 1/latency
        scores.update({tun: score})

    if active in scores:
        ascore = scores.pop(active) # Pop out active score to avoid comparing the active interface to itself
        for tun in scores: # Threshold represents the percentage a given score must beat the active int by to preempt
            if scores[tun] > (ascore * (1 + config["threshold"])):
                return tun

    return None

# Script entry point
mib = Store("MIB.json")
config = Store("config.json").read() # Config is read-only

while True:
    print("Polling agent:")
    data = agent.poll(10)
    for tun in data:
        tun.update({"time": str(time.strftime("%d/%m %H:%M:%S"))}) # Append time here to account for transmission time
        if tun["int"] in mib.read():
            lis = mib.read(tun["int"])
        else:
            lis = []
        lis.insert(0, tun) # Prepend the value to the list
        mib[tun.pop("int")] = lis

    print("Generating graph....", end="")
    graphing.genGraph(mib.read())
    print("done")

    print("Making a decision....", end="")
    tun = pickTun(mib.read(), config)
    if tun is not None:
        print(f"switching to {tun}")
        runCMD(f"./scripts/switchTuns.sh {tun}")
    else:
        print(f"not switching interface")
    print("done")

    print("Sleeping...")
    time.sleep(config["delay"])
