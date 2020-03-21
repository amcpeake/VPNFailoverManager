import json
#import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


with open('testData.json', 'r') as testData:
	data=json.load(testData)


# Get all data from JSON file.
dates = [i['time'] for i in data["data"]]
latency = [i['latency'] for i in data['data']]
download = [i['download'] for i in data['data']]
upload = [i['upload'] for i in data['data']]


fig, axes = plt.subplots(2, 1)

axes[0].set_title('Recorded Speeds')
axes[0].plot(dates, download)

axes[0].plot(dates, upload)
axes[0].set_ylabel('Speed (Mbps)')


axes[1].set_title('Recorded Latency')
axes[1].plot(dates, latency)
axes[1].set_ylabel('Latency (ms)')


#Enable legend titles
axes[0].legend(['Download', 'Upload'])
axes[1].legend(['Latency'])

#Generate Visual
plt.show()