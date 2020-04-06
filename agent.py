import subprocess
import time


def runCMD(cmd): # Run a command and return stdout as a string
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ps.communicate()[0].decode('utf-8')


def setTun(tun): # Switch the interface
    runCMD(f"./scripts/switchTuns.sh {tun}")


def poll(fsize = 10): # Optional parameter to manually set filesize for bandwidth tests
    tunnels = runCMD("ip link | awk '{print $2}' | grep -oE 'tun[0-9]+'").split("\n")[:-1]
    measurements = []
    for tun in tunnels:
        data = {"int": tun}
        print(f"\t{tun} - Measuring latency....", end="")
        data["latency"] = round(sum(float(i) for i in
                      runCMD(f"ping 8.8.8.8 -c 4 -I {tun} | grep -oE \"time=[0-9.]+\" | cut -d'=' -f2")
                      .split("\n")[:-1]) / 4.0, 3)
        print(f"{data['latency']}ms")

        print(f"\t{tun} - Measuring download speed ({fsize} MB file)....", end="")
        start = time.time()
        runCMD(f"curl -o test.zip http://speedtest.wdc01.softlayer.com/downloads/test{fsize}.zip --interface {tun} &> /dev/null")
        data["download"] = round((fsize * 8) / (time.time() - start), 2) # Use time to download to calc Mbps
        print(f"{data['download']}Mbps")

        print(f"\t{tun} - Measuring upload speed ({fsize} MB file....", end="")
        start = time.time()
        runCMD(f"curl -T test.zip filebin.net --interface {tun} &> /dev/null")
        data["upload"] = round((fsize * 8) / (time.time() - start), 2)
        print(f"{data['upload']}Mbps")

        measurements.append(data)
    return measurements