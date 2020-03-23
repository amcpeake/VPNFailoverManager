import os
import re
import json
import time
from datetime import datetime


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
    with open('output.txt', 'w') as r:
        jsonList = []
        for i, ip in enumerate(IP):
            os.system('ping %s -c 4 > ping.txt' % ip)


            start_timeDn = time.time()
            os.system('sudo /home/oyuen/PycharmProjects/getNetStats/wget.sh --interface tun% down' % i)
            # os.system('sudo /home/oyuen/PycharmProjects/getNetStats/wget.sh --interface tun0 down')
            end_timeDn = time.time()
            total_timeDn = end_timeDn - start_timeDn
            rounded_timeDn = "%.3f" % round(total_timeDn, 3)
            dl_bw = float(100) / float(rounded_timeDn)
            print('Download Bandwidth: ', dl_bw, 'mbps')

            start_timeUp = time.time()
            os.system('sudo /home/oyuen/PycharmProjects/getNetStats/wget.sh --interface tun% up' % i)
            # os.system('sudo /home/oyuen/PycharmProjects/getNetStats/wget.sh --interface tun0 up')
            end_timeUp = time.time()
            total_timeUp = end_timeUp - start_timeUp
            rounded_timeUp = "%.3f" % round(total_timeUp, 3)
            up_bw = float(100) / float(rounded_timeUp)
            print('Upload Bandwidth: ', up_bw, 'mbps')

            with open('ping.txt') as f:
                rttList = []
                lines = f.readlines()
                rttList.append(lines[-1])
                rtt = rttList[0].split("/")
                print('Average round trip time is: ', rtt[4], 'ms')

                now = datetime.now()
                print('The current time is: ', now)
                cur_time = str(now)

                data = {'data' + str(i): []}
                data['data' + str(i)].append({
                    'latency': rtt[4],
                    'download': dl_bw,
                    'upload': up_bw,
                    'time': cur_time
                })
                jsonList.append(data)

        json.dump(jsonList, r, indent=2)


if __name__ == "__main__":
    main()
