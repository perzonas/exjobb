
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
        if 50 < cur_time < 51:
            print("### 50 Seconds elapsed on test. ###")
            time.sleep(1)
        if 100 < cur_time < 101:
            print("### 100 Seconds elapsed on test and I'm still working on it. ###")
            time.sleep(1)
        if 150 < cur_time < 151:
            print("### 150 Seconds elapsed on test, hard work. ###")
            time.sleep(1)
        if 200 < cur_time < 201:
            print("### 200 Seconds elapsed on test, I'm exhausted. ###")
            time.sleep(1)
        if 250 < cur_time < 251:
            print("### 250 Seconds elapsed on test, still here. ###")
            time.sleep(1)
        if 300 < cur_time < 301:
            print("### 300 Seconds elapsed on test, just waiting for convergence now..... ###")
            time.sleep(1)
        if time.time()-starttime < 300:
            for i in range(1, hosts+1):
                args = [host + str(i), switch, down]


                if i % 2 == 0:
                    if loops < 3:
                        print("Connection to Host %s lost." % str(i))
                        network.configLinkStatus(*args)
                        time.sleep(seconds/3)
                        args[2] = up
                        network.configLinkStatus(*args)
                        print("Connection to Host %s reestablished.\n Elapsed time: %s" % (
                            str(i), str(time.time() - starttime)))
                elif i % 2 != 0:
                    if loops < 2:
                        print("Connection to Host %s lost." % str(i))
                        network.configLinkStatus(*args)
                        time.sleep(seconds/2)
                        args[2] = up
                        network.configLinkStatus(*args)
                        print("Connection to Host %s reestablished.\n Elapsed time: %s" % (
                            str(i), str(time.time() - starttime)))
                if time.time()-starttime >= 300:
                    break

        else:

            if consistensycheck(hosts, type):
                con_time = time.time()-starttime
                print("Reached consistency after %f seconds." % con_time)
                path = "results/convergetime-%d-%d" % (type, hosts)
                file = open(path, "w")
                os.chmod(path, 0o777)
                file.write(str(con_time))
                file.close()
                break





        loops += 1








    ### Found the function in the source code that changes the state of a connection to up/down it takes a list of 3
    # elements ["Host1", "Switch1", "up/down"] to change the link between host1 and the switch
    # network.configLinkStatus( *args )


