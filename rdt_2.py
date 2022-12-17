# The Transport Layer simulation (using Reliable Data Transport (rdt) protocol)
# rdt_2.0

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
import sys


STATE_0 = 0  # sender waiting for message from above
STATE_1 = 1  # sender waiting for ACK or NAK


class rdt_sender(object):
    def __init__(self, env):
        self.env = env
        self.channel = None
        self.seq_num = 0

        self.state = STATE_0
        self.pkt = None

    def rdt_send(self, msg):

        if self.state == STATE_0:
            # create a packet
            # send it through the channel udt_send() method
            # confirm to the upper layer the sent message

            self.pkt = packet(seq_num=self.seq_num, payload=msg)
            self.seq_num += 1
            print("TIME: ", self.env.now, ": RDT_SENDER:  send pkt ", msg)

            self.channel.udt_send(self.pkt)
            self.state = STATE_1  # switch to the second state, waiting for ACK
            return True
        else:
            return False

    def rdt_rcv(self, pkt):
        # in other versions of the rdt protocol.. you will need a method that will
        # handle the incoming packets from the receivers
        # in specific (ACK and NAK messages)
        assert self.state == STATE_1

        if pkt.payload == "ACK":
            self.state = STATE_0
        elif pkt.payload == "NAK":
            self.channel.udt_send(self.pkt)  # re-send the last un-acknowledged packet
        else:
            print("ERROR in rdt_rcv() - corrupted!!")
            print("stopping simulation...")
            sys.exit(0)


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

        if pkt.corrupted:
            # send back NAK..
            response = packet(seq_num=0, payload="NAK")
            self.channel.udt_send(response)

        else:
            response = packet(seq_num=0, payload="ACK")
            self.channel.udt_send(response)
            self.ReceiverAPP.deliver_data(pkt.payload)
