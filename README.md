# VPNFailoverManager
VPNFailoverManager is a series of python scripts that loosely mirror SNMP's manager/agent operation.

A manager script "polls" the agent for information about its current VPN connections (latency, and bandwidth) at a given interval. The manager then uses that data to inform the agent whether or not it has a better VPN connection available, at which point the agent will change its active connection.

Note: Polling measurements are done in sequence. This is because, for testing purposes, VPN tunnels (virtual interfaces) are used over a single physical interface. If the VPN tunnels were measured in parallel, measuring one tunnel would influence the measurements of another.

If using physical NICs, measuring in parallel would be preferable for efficiency.

## JSON Files
### Config
config.json can be edited by the "manager" or the "agent" user but is read-only in the context of the scripts. It contains weights which are applied to the connection measurement values to score each interface. There is also a depth value which denotes how many past measurements to consider when scoring an interface. Finally there is a threshold value, which is the percetange by which an interface's score must be greater than the current interface's score to force the agent to change its active connection.

### MIB
MIB.json stores the measurements returned by the agent, organized per interface in the following form:

`{ <tunnel name>: [{"latency": X, "download": X, ...}, ...], <tunnel name>: [{}]... }`



## Agent
### Parameters
fsize (default 100) - The file size to use for download / upload speed tests to use. Can be 10, or 100. Higher is more accurate but slower
### Results
Returns json in the following form: 

`[{"int": <tunnel name>, "latency": X, "download": X, "upload": X}, {"int": <tunnel name>...}...]`

### Function
The agent first gathers a list of available tunnels, and then one by one uses them to gather various pieces of information.

Latency is measured by pinging 8.8.8.8 (Google's DNS, used for its nearly 100% uptime) and averaging the RTT time over 4 pings

Bandwidth is measured by using curl to first downloading a zip file of a given size (10MB or 100MB) from speedtest.net then uploading it to filebin.net, measuring the total time each operation took, and calculating an overal Mbps value.

The agent then returns a list of measurements it took (one per interface)

## Manager
### Parameters
Uses values in config.json to calculate a score for each tunnel

### Results
Calls graphing.py which in turn generates a graph, and may call switchTuns.sh which will force the agent to switch interfaces (if warranted)

### Function
The manager first initializes two instances of the `Store` class found in `syncStore.py`. This is simply a class which simplifies syncronization of data between an in memory dictionary and a JSON file containing the JSON representation of said dictionary. One for `MIB.json` and one for `config.json`

The manager then polls the agent, and waits for its response. It will then add a timestamp for each measurement (used for graphing) and send the entire `MIB.json` to `graphing.py` to generate a new up-to-date graph.

Next the manager uses the depth value in `config.json` to read that many past measurements from `MIB.json` per interface. If that many measurements do not exist for a given interface it is not given a score and is therefore not eligible to be switched to. Using weight values for each parameter (latency and bandwidth) found in `config.json`, each valid interface is given a score. Finally each score is compared to the score of the current active interface, and if it is greater than the active score by a factor denoted by the threshold value in `config.json`, it becomes the new active interface.

Finally, the manager script sleeps for a time denoted by the delay value in `config.json` and repeats the entire process again


