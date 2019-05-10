
from mininet.net import Mininet
from mininet.util import dumpNodeConnections, irange, quietRun, irange
from mininet.log import setLogLevel, lg, info
from mininet.node import UserSwitch, OVSKernelSwitch, Controller, OVSSwitch, CPULimitedHost, RemoteController
from mininet.link import TCLink, TCIntf, Intf
from mininet.term import makeTerm, cleanUpScreens  # Open xterm from mininet
from functools import partial
from mininet.cli import CLI
from linkConnections import *
import time


def linkScript(network, hosts):
    switch = "Switch1"
    up = "up"
    down = "down"
    host = "Host"
    loops = 0
    starttime = time.time()
    while time.time()-starttime < 300:
        for i in range(1, hosts+1):
            args = [host + str(i), switch, down]
            if not (i % 2 == 0 and loops == 2):
                network.configLinkStatus(*args)
                print("Connection to Host %s lost." % str(i))
                if i % 2 == 0 and loops < 2:
                    time.sleep(3)
                elif i % 2 != 0 and loops < 3:
                    time.sleep(2)
                args[2] = up
                network.configLinkStatus(*args)
                print("Connection to Host %s reestablished." % str(i))
                time.sleep(i)
        loops += 1








    ### Found the function in the source code that changes the state of a connection to up/down it takes a list of 3
    # elements ["Host1", "Switch1", "up/down"] to change the link between host1 and the switch
    # network.configLinkStatus( *args )


