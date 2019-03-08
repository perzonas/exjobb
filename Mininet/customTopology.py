import sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections, irange, quietRun, irange
from mininet.log import setLogLevel, lg, info
from mininet.node import UserSwitch, OVSKernelSwitch, Controller, OVSSwitch, CPULimitedHost, RemoteController
from mininet.link import TCLink, TCIntf, Intf
from mininet.term import makeTerm, cleanUpScreens  # Open xterm from mininet
from functools import partial
from mininet.cli import CLI


class CustomTopo(Topo):

    def build(self, no_of_hosts, cpu=0.5, cores=2):
        hosts = [self.addHost("Host%s" % h, cpu=cpu, cores=cores, ip=("20.1.90.%d/24" % h)) for h in range(1, no_of_hosts+1)]
        switch = self.addSwitch("Switch1")

        for host in hosts:
            self.addLink(host, switch)


topos = {'customtopo': (lambda: CustomTopo())}


class CustomTopology:

    def startBackend(self, server, hosts):

        # makeTerm(node=server, cmd="python backend/backend.py %s %d" % (server.IP().replace("10.1.0.",""), nbOfServers) )
        makeTerm(node=server, cmd="python backend/backend.py %s" % hosts)

    def setup(self, no_of_hosts=10, bandwidth=1000, delay='5ms', loss=1, queue_size=1000):

        topology = CustomTopo(no_of_hosts)
        # Select TCP Reno
        # output = quietRun('sysctl -w net.ipv4.tcp_congestion_control=reno')
        # assert 'reno' in output

        links = partial(TCLink, delay=delay, bw=bandwidth, loss=loss, max_queue_size=queue_size, use_htb=True)
        ovsswitch = partial(OVSSwitch, protocol='OpenFlow13')

        # remoteController = partial(RemoteController, ip='127.0.0.1', port=6653)
        # Set the topology, the class for links and interfaces, the mininet environment must be cleaned up before
        # launching, we should build now the topology
        network = Mininet(topo=topology, switch=ovsswitch, controller=Controller, intf=TCIntf,
                          host=CPULimitedHost, link=links, cleanup=True, build=True, ipBase='20.1.90.0/24')

        network.start()

        info("*** Dumping host connections\n")
        dumpNodeConnections(network.hosts)

        info("*** testing basic connectivity\n")
        # network.pingAll()

        info("*** testing bandwith between host 1 & 2\n")
        h1, h2 = network.get('Host1', 'Host2')
        # network.iperf((h1, h2))

        for host in network.hosts:
            print(host.IP())
            self.startBackend(host, host.name[-1])

        CLI(network)

        network.stop()

        # We close the xterms (mininet.term.cleanUpScreens)
        cleanUpScreens()


if __name__ == '__main__':
    setLogLevel('info')
    simulation = CustomTopology()
    if len(sys.argv) == 1:
        simulation.setup()
    else:
        hosts = int(sys.argv[1])
        simulation.setup(hosts)

