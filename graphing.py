import json
import matplotlib.pyplot as plt


# Get all data from file.
def genGraph(data):
	tuns = []
	for tun in data:
		tuns.append({tun: {
				"time": list(i["time"] for i in data[tun]),
				"latency": list(i["latency"] for i in data[tun]),
				"download": list(i["download"] for i in data[tun]),
				"upload": list(i["upload"] for i in data[tun])
			}
		})

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