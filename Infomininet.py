############################################################

# A Mininet network consists of the following components:

# Isolated Hosts. An emulated host in Mininet is a group of user-level processes moved into a network namespace -
# a container for network state. Network namespaces provide process groups with exclusive ownership of interfaces,
# ports, and routing tables (such as ARP and IP). For example, two web servers in two network namespaces can coexist
# on one system, both listening to private eth0 interfaces on port 80. Mininet uses CPU Bandwidth Limiting to limit
# the fraction of a CPU available to each process group.

# Emulated Links. The data rate of each link is enforced by Linux Traffic Control (tc), which has a number of packet
# schedulers to shape traffic to a configured rate. Each emulated host has its own virtual Ethernet interface(s)
# (created and installed with ip link add/set). A virtual Ethernet (or veth) pair, acts like a wire connecting
# two virtual interfaces, or virtual switch ports; packets sent through one interface are delivered to the other,
# and each interface appears as a fully functional Ethernet port to all system and application software.

# Emulated Switches. Mininet typically uses the default Linux bridge or Open vSwitch running in kernel mode to switch
# packets across interfaces. Switches and routers can run in the kernel (for speed) or in user space (so we can
# modify them easily).

#############################################################

# self.addHost(name, cpu=f):

# This allows you to specify a fraction of overall system CPU resources which will be allocated to the virtual host.

# self.addLink(node1, node2, bw=10, delay='5ms', max_queue_size=1000, loss=10, use_htb=True): adds a bidirectional link
# with bandwidth, delay and loss characteristics, with a maximum queue size of 1000 packets using the Hierarchical
# Token Bucket rate limiter and netem delay / loss emulator.
# The parameter bw is expressed as a number in Mbit;
# delay is expressed as a string with units in place (e.g.'5ms', '100us', '1s');
# loss is expressed as a percentage (between 0 and 100);
# and max_queue_size is expressed in packets.


# Unlike a simulator, Mininet doesn't have a strong notion of virtual time; this means that timing measurements will
# be based on real time, and that faster-than-real-time results (e.g. 100 Gbps networks) cannot easily be emulated.

# An aside on performance: The main thing you have to keep in mind for network- limited experiments is that you will
# probably need to use slower links, for example 10 or 100 Mb/sec rather than 10 Gb/sec, due to the fact that packets
# are forwarded by a collection of software switches (e.g. Open vSwitch) that share CPU and memory resources and usually
# have lower performance than dedicated switching hardware. For CPU-limited experiments, you will also need to make
# sure that you carefully limit the CPU bandwidth of your Mininet hosts. If you mainly care about functional
# correctness, you can run Mininet without specific bandwidth limits - this is the quick and easy way to run Mininet,
# and it also provides the highest performance at the expense of timing accuracy under load.





# In the Mininet documentation it's possible to __init__ the CLI mode with a script. Each line of the script will
# be executed within the CLI, without stopping for user input. A cursory glance in this documentation reveals the
# individual methods the CLI uses to interpret and execute commands.

# Here is an example:

# myScript = "genTraffic.sh"
# CLI(net, script=myScript) # Batch mode script execution
# CLI(net) # Send user in the CLI for additional manual actions
# The script I use is the same as the one posted in the question, with prepended Pings to let the network controller
# and Mininet some time to "see" each other.

# h1 ping h5 -c 3
# h2 ping h6 -c 3
# h5 iperf3 -s -p 1337 &
# h6 iperf3 -s -p 1338 &
# h1 iperf3 -c h5 -n 10G -b 11M -p 1337 &
# h2 iperf3 -c h6 -n 10G -b 11M -p 1338 &


