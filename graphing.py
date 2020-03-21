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

plt.plot(dates, latency, label='Latency')

plt.plot(dates, download, label='Download')

plt.plot(dates, upload, label='Upload')

# Labeling the graph.
plt.xlabel('Timestamp')
plt.ylabel('Speed (mpbs)')

plt.title('Recorded Statistics')
plt.legend()

# Show the graph
plt.show()