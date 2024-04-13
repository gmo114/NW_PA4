from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, IPAddr6, EthAddr

log = core.getLogger()

#statically allocate a routing table for hosts
#MACs used in only in part 4
IPS = {
  "h10" : ("10.0.1.10", '00:00:00:00:00:01'),
  "h20" : ("10.0.2.20", '00:00:00:00:00:02'),
  "h30" : ("10.0.3.30", '00:00:00:00:00:03'),
  "serv1" : ("10.0.4.10", '00:00:00:00:00:04'),
  "hnotrust" : ("172.16.10.100", '00:00:00:00:00:05'),
}

class Part3Controller (object):
  """
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    print (connection.dpid)
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)
    #use the dpid to figure out what switch is being created
    if (connection.dpid == 1):
      self.s1_setup()
    elif (connection.dpid == 2):
      self.s2_setup()
    elif (connection.dpid == 3):
      self.s3_setup()
    elif (connection.dpid == 21):
      self.cores21_setup()
    elif (connection.dpid == 31):
      self.dcs31_setup()
    else:
      print ("UNKNOWN SWITCH")
      exit(1)

  def s1_setup(self):
    #put switch 1 rules here
    msg = of.ofp_flow_mod()
    msg.priority = 0xFFFF
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))  # Sends packets on all ports but the input port
    self.connection.send(msg)  # accept

  def s2_setup(self):
    # put switch 2 rules here
    msg = of.ofp_flow_mod()
    msg.priority = 0xFFFF
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))  # Sends packets on all ports but the input port
    self.connection.send(msg)  # accept

  def s3_setup(self):
    # put switch 3 rules here
    msg = of.ofp_flow_mod()
    msg.priority = 0xFFFF
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))  # Sends packets on all ports but the input port
    self.connection.send(msg)  # accept

  def cores21_setup(self):

    msg = of.ofp_flow_mod()
    msg.priority = 0xFFFF
    msg.match.dl_type = 0x0806  # ARP protocol
    msg.match.nw_src = IPS.get("hnotrust")[0]
    msg.match.nw_dst = IPS.get("serv1")[0]
    self.connection.send(msg)  # accept

    msg = of.ofp_flow_mod()
    msg.priority = 0xFFFF
    msg.match.dl_type = 0x0806  # ARP protocol
    msg.match.nw_src = IPS.get("serv1")[0]
    msg.match.nw_dst = IPS.get("hnotrust")[0]
    self.connection.send(msg)  # accept

    msg = of.ofp_flow_mod()
    msg.priority = 0xFFFF
    msg.match.dl_type = 0x0800  # if ip ( ipv4 )
    msg.match.nw_src = IPS.get("hnotrust")[0]
    msg.match.nw_proto = 1  # IP Protocol  ( icmp )
    self.connection.send(msg)  # reject

    msg = of.ofp_flow_mod()
    msg.priority = 0xFFFF
    msg.match.dl_type = 0x0800  # if ip ( ipv4 )
    msg.match.nw_dst = IPS.get("hnotrust")[0]
    msg.match.nw_proto = 1  # IP Protocol  ( icmp )
    self.connection.send(msg)  # reject

    ip_to_port1 = [(IPS.get("h20")[0], 2), (IPS.get("h30")[0], 3), (IPS.get("serv1")[0], 4)]
    ip_to_port2 = [(IPS.get("h10")[0], 1), (IPS.get("h30")[0], 3), (IPS.get("serv1")[0], 4)]
    ip_to_port3 = [(IPS.get("h10")[0], 1), (IPS.get("h20")[0], 2), (IPS.get("serv1")[0], 4)]
    ip_to_port4 = [(IPS.get("h10")[0], 1), (IPS.get("h20")[0], 2), (IPS.get("h30")[0], 3)]
    all_ip_to_port = [ip_to_port1, ip_to_port2, ip_to_port3, ip_to_port4]
    src_num = 0
    port_send = 0
    for ip_to_port in all_ip_to_port:
        src = ["h10", "h20", "h30", "serv1"]
        for info in ip_to_port:
            msg = of.ofp_flow_mod()
            msg.priority = 0xFFFF
            msg.match.dl_type = 0x0806  # ARP protocol
            msg.match.nw_src = IPS.get(src[src_num])[0]
            msg.match.nw_dst = info[0]
            msg.actions.append(of.ofp_action_output(port=info[1]))  # Sends packets on all ports but the input port
            self.connection.send(msg)  # accept

            msg = of.ofp_flow_mod()
            msg.priority = 0xFFFF
            msg.match.dl_type = 0x0800  # if ip ( ipv4 )
            msg.match.nw_src = IPS.get(src[src_num])[0]
            msg.match.nw_dst = info[0]
            msg.match.nw_proto = 1  # IP Protocol  ( icmp )
            msg.actions.append(of.ofp_action_output(port=info[1]))  # Sends packets on all ports but the input port
            self.connection.send(msg)  # accept

            msg = of.ofp_flow_mod()
            msg.priority = 0xFFFF
            msg.match.dl_type = 0x0800  # if ip ( ipv4 )
            msg.match.nw_src = IPS.get(src[src_num])[0]
            msg.match.nw_dst = info[0]
            msg.actions.append(of.ofp_action_output(port=info[1]))  # Sends packets on all ports but the input port
            self.connection.send(msg)  # accept

        if src[src_num] != "serv1":
            msg = of.ofp_flow_mod()
            msg.priority = 0xFFFF
            msg.match.dl_type = 0x0806  # ARP protocol
            msg.match.nw_src = IPS.get("hnotrust")[0]
            msg.match.nw_dst = IPS.get(src[src_num])[0]
            if src[src_num] == 'h10':
                port_send = 1
            elif src[src_num] == 'h20':
                port_send = 2
            else:
                port_send = 3
            msg.actions.append(of.ofp_action_output(port=port_send))
            self.connection.send(msg)  # accept

            msg = of.ofp_flow_mod()
            msg.priority = 0xFFFF
            msg.match.dl_type = 0x0800  # if ip ( ipv4 )
            msg.match.nw_src = IPS.get(src[src_num])[0]
            msg.match.nw_dst = IPS.get(src[src_num])[0]
            msg.actions.append(of.ofp_action_output(port=port_send))  # Sends packets on all ports but the input port
            self.connection.send(msg)  # accept

            msg = of.ofp_flow_mod()
            msg.priority = 0xFFFF
            msg.match.dl_type = 0x0806  # ARP protocol
            msg.match.nw_src = IPS.get(src[src_num])[0]
            msg.match.nw_dst = IPS.get("hnotrust")[0]
            msg.actions.append(of.ofp_action_output(port=5))
            self.connection.send(msg)  # accept

        src_num = src_num + 1

    msg = of.ofp_flow_mod()
    self.connection.send(msg)  # drops

  def dcs31_setup(self):
    # put datacenter switch rules here
    msg = of.ofp_flow_mod()
    msg.priority = 0xFFFF
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))  # Sends packets on all ports but the input port
    self.connection.send(msg)  # accept

  #used in part 4 to handle individual ARP packets
  #not needed for part 3 (USE RULES!)
  #causes the switch to output packet_in on out_port
  def resend_packet(self, packet_in, out_port):
    msg = of.ofp_packet_out()
    msg.data = packet_in
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)
    self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Packets not handled by the router rules will be
    forwarded to this method to be handled by the controller
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    print ("Unhandled packet from " + str(self.connection.dpid) + ":" + packet.dump())

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Part3Controller(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
