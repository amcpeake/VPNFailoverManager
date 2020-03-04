import os
import re
import json


def getIP():
    IP = []
    os.system('ifconfig > ifconf.txt')

    with open("ifconf.txt") as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if re.match('tun[0-9]+', line):
                ipLine = lines[i + 1]
                ipFields = ipLine.split()

                IP.append((ipFields[1]))

        return (IP)


def main():
    IP = getIP()
    with open('rtt.txt', 'w') as r:
        jsonList = []
        for i, ip in enumerate(IP):
            os.system('ping %s -c 4 > latency.txt' % ip)

            with open('latency.txt') as f:
                rttList = []
                lines = f.readlines()
                print(lines[-1])
                rttList.append(lines[-1])
                rtt = rttList[0].split("/")

                data = {'rtt' + str(i): []}
                data['rtt' + str(i)].append({
                    'minRTT': rtt[3][-5:],
                    'avgRTT': rtt[4],
                    'maxRTT': rtt[5],
                    'mDEV': rtt[6][:5]
                })

                jsonList.append(data)

        json.dump(jsonList, r, indent=2)


if __name__ == "__main__":
    main()
