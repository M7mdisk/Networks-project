# The Transport Layer simulation (using Reliable Data Transport (rdt) protocol)
# rdt_1.0

# Sender Transport Layer
# rdt_sender
# - receive message from the application layer
# - run the rdt_1.0 protocol using udt_send() method


# Receiver Transport Layer
# rdt_reecieve
# - receive packet from the underlaying channel (lower layer) through rdt_rcv() method
# - delivers the packet to the upper layer (applicaiton layer)


import simpy
import random
from packet import packet


class rdt_sender(object):
    def __init__(self, env):
        self.env = env
        self.channel = None
        self.seq_num = 0
        self.pkt = None

    def rdt_send(self, msg):
        # create a packet
        # send it through the channel udt_send() method
        # confirm to the upper layer the sent message

        pkt = packet(seq_num=self.seq_num, payload=msg)
        self.seq_num += 1

        print("TIME: ", self.env.now, ": RDT_SENDER:  send pkt ", msg)

        self.channel.udt_send(pkt)
        return True

    def rdt_rcv(self, pkt):
        # in other versions of the rdt protocol.. you will need a method that will
        # handle the incoming packets from the receivers
        # in specific (ACK and NAK messages)
        print("not yet implemented!!!!")
        pass


class rdt_receiver(object):
    def __init__(self, env):
        self.env = env
        self.ReceiverAPP = None
        self.channel = None

    def rdt_rcv(self, pkt):

        # received a packet from lower layer
        # check for corruption, then
        # deliver the packet to upper layer method deliver_data()
        print("TIME: ", self.env.now, ": RDT_RECEIVER:  Receive pkt ", pkt.payload)

        if not (pkt.corrupted):
            self.ReceiverAPP.deliver_data(pkt.payload)
