from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI

class CustomSingleTopo(Topo):
    def build(self, no_hosts=4):
        hosts = [self.addHost("host%s" % (h+1)) for h in range(no_hosts)]
        switch = self.addSwitch("Switch1")

        for host in hosts:
            self.addLink(host, switch)


topos = {'customsingletopo': (lambda: CustomSingleTopo())}

singleswitch = CustomSingleTopo(4)
net = Mininet(topo=singleswitch)
net.start()
CLI(net)
net.stop()