
from mininet.net import Mininet
from mininet.util import dumpNodeConnections, irange, quietRun, irange
from mininet.log import setLogLevel, lg, info
from mininet.node import UserSwitch, OVSKernelSwitch, Controller, OVSSwitch, CPULimitedHost, RemoteController
from mininet.link import TCLink, TCIntf, Intf
from mininet.term import makeTerm, cleanUpScreens  # Open xterm from mininet
from functools import partial
from mininet.cli import CLI
import time
from aftertest import *


def linkScript(network, hosts, seconds, type):
    print("----------------------------\n STARTING linkScript\n ----------------------------")
    switch = "Switch1"
    up = "up"
    down = "down"
    host = "Host"
    loops = 0
    starttime = time.time()
    while True:
        cur_time = time.time() - starttime
        if cur_time % 10 == 0:
            print("Elapsed time on test: ", cur_time)

        if time.time()-starttime > 300:
            if consistensycheck(hosts, type):
                con_time = time.time()-starttime
                print("Reached consistency after %f seconds." % con_time)
                path = "results/convergetime-%d-%d" % (type, hosts)
                file = open(path, "w")
                os.chmod(path, 0o777)
                file.write(str(con_time))
                file.close()
                break

        if cur_time % 300 < 5:
            for j in range(3):
                for i in range(1, hosts+1):
                    args = [host + str(i), switch, down]
                    if time.time() - starttime > 300:
                        if consistensycheck(hosts, type):
                            j = 99
                            break


                    if i % 2 == 0:
                        print("Connection to Host %s lost." % str(i))
                        network.configLinkStatus(*args)
                        time.sleep(seconds/3)
                        args[2] = up
                        network.configLinkStatus(*args)
                        print("Connection to Host %s reestablished.\n Elapsed time: %s" % (
                            str(i), str(time.time() - starttime)))
                    elif i % 2 != 0:
                        if j < 2:
                            print("Connection to Host %s lost." % str(i))
                            network.configLinkStatus(*args)
                            time.sleep(seconds/2)
                            args[2] = up
                            network.configLinkStatus(*args)
                            print("Connection to Host %s reestablished.\n Elapsed time: %s" % (
                                str(i), str(time.time() - starttime)))
                if j == 99:
                    print("J IS 99")
                    break













    ### Found the function in the source code that changes the state of a connection to up/down it takes a list of 3
    # elements ["Host1", "Switch1", "up/down"] to change the link between host1 and the switch
    # network.configLinkStatus( *args )


