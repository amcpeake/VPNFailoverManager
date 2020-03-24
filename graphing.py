import json
import matplotlib.pyplot as plt


# Get all data from file.
def genGraph(file):
	times = []
	latency = []
	download = []
	upload = []
	with open(file, 'r') as f:
		for line in f:
			print(line)
			data = json.loads(line)
			times.extend([i['time'] for i in data])
			latency.extend([i['latency'] for i in data])
			download.extend([i['download'] for i in data])
			upload.extend([i['upload'] for i in data])

	fig, axes = plt.subplots(2, 1)

	axes[0].set_title('Recorded Speeds')
	axes[0].plot(times, download)

	axes[0].plot(times, upload)
	axes[0].set_ylabel('Speed (Mbps)')


	axes[1].set_title('Recorded Latency')
	axes[1].plot(times, latency)
	axes[1].set_ylabel('Latency (ms)')


	#Enable legend titles
	axes[0].legend(['Download', 'Upload'])
	axes[1].legend(['Latency'])

	#Generate Visual
	plt.savefig('graph.png')