import json
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


with open('testData.json', 'r') as testData:
	data=json.load(testData)

dates = [i['time'] for i in data["data"]]
latency = [i['latency'] for i in data['data']]
download = [i['download'] for i in data['data']]
upload = [i['upload'] for i in data['data']]




df = pd.DataFrame({'dates':dates, 'latency':latency})
df['dates']  = [pd.to_datetime(i) for i in df['dates']]

plt.bar(dates, latency)
plt.show()