############################################################

A Mininet network consists of the following components:

Isolated Hosts. An emulated host in Mininet is a group of user-level processes moved into a network namespace - a container for network state. Network namespaces provide process groups with exclusive ownership of interfaces, ports, and routing tables (such as ARP and IP). For example, two web servers in two network namespaces can coexist on one system, both listening to private eth0 interfaces on port 80. Mininet uses CPU Bandwidth Limiting to limit the fraction of a CPU available to each process group.

Emulated Links. The data rate of each link is enforced by Linux Traffic Control (tc), which has a number of packet schedulers to shape traffic to a configured rate. Each emulated host has its own virtual Ethernet interface(s) (created and installed with ip link add/set). A virtual Ethernet (or veth) pair, acts like a wire connecting two virtual interfaces, or virtual switch ports; packets sent through one interface are delivered to the other, and each interface appears as a fully functional Ethernet port to all system and application software.

Emulated Switches. Mininet typically uses the default Linux bridge or Open vSwitch running in kernel mode to switch packets across interfaces. Switches and routers can run in the kernel (for speed) or in user space (so we can modify them easily).

#############################################################
