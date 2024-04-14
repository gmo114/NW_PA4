PROJECT TITLE: Programming Assignment 4: Generalized Packet Forwarding in Software Defined Networking

PROJECT DESCRIPTION: Working with Mininet and Pox controller along with OpenFlow switches to create a different network
topologies, and firewalls. An SDN controller will be used to give the different OpenFlow switches flow rules on how to
handle the different packets that come to it. This gives the switches the ability to filter packets and as said before
act as a firewall.

INSTALL:
    Installing Mininet -> sudo apt install mininet
    Installing openvswitch -> sudo apt-get install openvswitch-testcontroller
                              sudo ln /usr/bin/ovs-testcontroller /usr/bin/ovs-controller
    Installing Pox Controller -> git clone http://github.com/noxrepo/pox
                                 cd pox
                                 git checkout dart
    Note for Pox Controller: You will need to install python 2.7 for the Pox Controller to work
                             -> sudo apt install python2.7

HOW TO USE TASK 1 - Custom Network Topology:
    A custom network topology that works as star topology.
    To run task 1 get in the same directory as part1.py and run with the following command
    -> sudo python3 part1.py
    Once running you can give mininet the following commands
    -> pingall
    This will show who all is reachable from each host
    -> dump
    Shows the connections between each host
    -> iperf
    Will show the TCP bandwidth between host

HOW TO USE TASK 2 - Simple Firewall:
    Simple firewall that will stop certain packets and allow other ones
    To run task 2 you must first move the part2controller.py into the ext directory in the pox directory.
    This directory will be in the home directory for your user account. With that in the correct directory you can
    run the following command to start the controller.
    -> ./pox.py part2controller
    This will start the controller that gives the switch flow rules.
    Note you must be in the pox directory
    -> sudo python3 part2.py
    You must be in the directory that contains the part2.py for this command to work.
    Once that is running mininet will open, and you can run the same commands from before to see how the firewall is
    working.
    -> pingall
    This will show who all is reachable from each host
    -> dump
    Shows the connections between each host
    -> iperf
    Will show the TCP bandwidth between host

HOW TO USE TASK 3 - Network Firewall:
    The set-up is the same as task 2 but this involves more flow rules and more host.
    To run task 3 you must first move the part3controller.py into the ext directory in the pox directory.
    This directory will be in the home directory for your user account. With that in the correct directory you can
    run the following command to start the controller.
    -> ./pox.py part3controller
    This will start the controller that gives the switch flow rules.
    Note you must be in the pox directory
    -> sudo python3 part3.py
    You must be in the directory that contains the part3.py for this command to work.
    Once that is running mininet will open, and you can run the same commands from before to see how the network
    firewall is working.
    -> pingall
    This will show who all is reachable from each host
    -> dump
    Shows the connections between each host
    -> iperf
    Will show the TCP bandwidth between host
