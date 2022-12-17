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


STATE_0 = 0  # sender waiting for message 0 from above
STATE_1 = 1  # sender waiting for ACK or NAK 0
STATE_2 = 2  # sender waiting for message 1 from above
STATE_3 = 3  # sender waiting for ACK or NAK 1


class rdt_sender:
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

            self.pkt = packet(seq_num=0, payload=msg)
            self.seq_num = 0
            self.channel.udt_send(self.pkt)
            self.state = STATE_1  # switch to the second state, waiting for ACK
            return True
        elif self.state == STATE_2:
            self.pkt = packet(seq_num=1, payload=msg)
            self.seq_num = 1
            self.channel.udt_send(self.pkt)
            self.state = STATE_3  # switch to the second state, waiting for ACK
            return True
        else:
            return False

    def rdt_rcv(self, pkt: packet):
        # in other versions of the rdt protocol.. you will need a method that will
        # handle the incoming packets from the receivers
        # in specific (ACK and NAK messages)
        if self.state not in [STATE_1, STATE_3]:
            return False
        if pkt.corrupted or pkt.payload == "NAK":
            print(
                "TIME: ",
                self.env.now,
                "SENDER RECIEVED NAK OR CORRUPTED Resending......",
            )
            self.channel.udt_send(self.pkt)
            return True
        elif (
            not pkt.corrupted
            and pkt.payload == "ACK"
            #  and pkt.sequ_num == self.seq_num
        ):
            self.seq_num = 1 - self.seq_num  # change packet number
            self.state = STATE_0 if self.state == STATE_3 else STATE_2
            return True


class rdt_receiver(object):
    def __init__(self, env):
        self.env = env
        self.ReceiverAPP = None
        self.channel = None
        self.state = 0

    def rdt_rcv(self, pkt: packet):
        if self.state == 0:
            if not pkt.corrupted and pkt.sequ_num == 0:
                response = packet(seq_num=0, payload="ACK")
                self.channel.udt_send(response)
                self.ReceiverAPP.deliver_data(pkt.payload)
                self.state = 1
                return True
            if pkt.corrupted:
                response = packet(seq_num=0, payload="NAK")
                self.channel.udt_send(response)
            elif pkt.sequ_num == 1:
                response = packet(seq_num=0, payload="ACK")
                self.channel.udt_send(response)
            return True
        elif self.state == 1:
            if not pkt.corrupted and pkt.sequ_num == 1:
                response = packet(seq_num=1, payload="ACK")
                self.channel.udt_send(response)
                self.ReceiverAPP.deliver_data(pkt.payload)
                self.state = 0
                return True
            if pkt.corrupted:
                response = packet(seq_num=1, payload="NAK")
                self.channel.udt_send(response)
            elif pkt.sequ_num == 0:
                response = packet(seq_num=1, payload="ACK")
                self.channel.udt_send(response)
            return True
        return False
