import matplotlib.pyplot as plt

# Get all data from file.
def genGraph(data):
  for tun in data:
    print(f"\nGraphing Tunnel {tun}....")
    time = list(i["time"] for i in data[tun])
    latency = list(i["latency"] for i in data[tun])
    download = list(i["download"] for i in data[tun])
    upload = list(i["upload"] for i in data[tun])

    fig, axes = plt.subplots(2, 1)
    # fig, axes = plt.subplots(figsize=(12,8))
    # reduce the number of x ticks. Not working
    # axes.locator_params(nbins=5)
    fig.suptitle(f"Recorded Stats: {tun}")
    fig.tight_layout(pad=5.0)
    
    axes[0].set_title('Speeds')
    axes[0].plot(time, download)
    axes[0].plot(time, upload)
    axes[0].set_ylabel('Speed (Mbps)')

    axes[1].set_title('Latency')
    axes[1].plot(time, latency)
    axes[1].set_ylabel('Latency (ms)')

    # Enable legend titles
    axes[0].legend(['Download', 'Upload'])
    axes[1].legend(['Latency'])
    
    # Generate Visual
  # plt.show()
    plt.savefig(f"graphs/graph-{tun}.png")
    
