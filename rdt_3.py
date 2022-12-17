# The Transport Layer simulation (using Reliable Data Transport (rdt) protocol)
# rdt_2.0

# Sender Transport Layer
# rdt_sender
# - receive message from the application layer
# - run the rdt_1.0 protocol using udt_send() method


# Receiver Transport Layer
# rdt_reecieve
# - receive Packet from the underlaying channel (lower layer) through rdt_rcv() method
# - delivers the Packet to the upper layer (applicaiton layer)


import simpy
import random
from packet import packet
import sys


STATE_0 = 0  # sender waiting for call 0 from above
STATE_1 = 1  # sender waiting for ACK0
STATE_2 = 2  # sender waiting for call 0 from above
STATE_3 = 3  # sender waiting for ACK1


class rdt_sender(object):
    def __init__(self, env):
        # Timer stuff
        self.env = env
        self.timeout_duration = 8
        self.timer_on = False
        self.timer = None

        self.channel = None
        self.seq_num = 0

        self.state = STATE_0
        self.pkt = None

    # This function models a Timer's behavior.
    def timer_behavior(self):
        assert self.state == 1 or self.state == 3
        try:
            self.timer_on = True
            yield self.env.timeout(self.timeout_duration)
            self.timer_on = False
            self.timeout_action()
        except simpy.Interrupt:
            self.timer_on = False

    def start_timer(self):
        assert self.timer_on == False
        self.timer = self.env.process(self.timer_behavior())

    def stop_timer(self):
        assert self.timer_on == True
        self.timer.interrupt()

    def timeout_action(self):
        assert self.state == STATE_1 or self.state == STATE_3
        print("TIMEOUT !!!!!!!!!")
        self.channel.udt_send(self.pkt)
        self.start_timer()

    def rdt_send(self, msg):
        if self.state == STATE_0:
            self.pkt = packet(seq_num=0, payload=msg)
            self.channel.udt_send(self.pkt)
            self.start_timer()
            self.state = STATE_1
        elif self.state == STATE_2:
            self.pkt = packet(seq_num=1, payload=msg)
            self.channel.udt_send(self.pkt)
            self.start_timer()
            self.state = STATE_3
        else:
            return False
        return True

    def rdt_rcv(self, pkt: packet):
        if self.state == STATE_0 or self.state == STATE_2:
            return False

        if self.state == STATE_1:
            if pkt.corrupted or (pkt.payload == "ACK" and pkt.sequ_num == 1):
                return True
            if not pkt.corrupted and (pkt.payload == "ACK" and pkt.sequ_num == 0):
                self.stop_timer()
                self.state = STATE_2
                return True
        elif self.state == STATE_3:
            if pkt.corrupted or (pkt.payload == "ACK" and pkt.sequ_num == 0):
                return True
            if not pkt.corrupted and (pkt.payload == "ACK" and pkt.sequ_num == 1):
                self.stop_timer()
                self.state = STATE_0
                return True


class rdt_receiver(object):
    def __init__(self, env):
        self.env = env
        self.ReceiverAPP = None
        self.channel = None
        self.state = STATE_0

    def rdt_rcv(self, pkt: packet):
        if self.state == 0:
            if not pkt.corrupted and pkt.sequ_num == 0:
                response = packet(seq_num=0, payload="ACK")
                self.channel.udt_send(response)
                self.ReceiverAPP.deliver_data(pkt.payload)
                self.state = STATE_1
                return True
            if pkt.corrupted or pkt.sequ_num == 1:
                response = packet(seq_num=1, payload="ACK")
                self.channel.udt_send(response)
            return True
        elif self.state == 1:
            if not pkt.corrupted and pkt.sequ_num == 1:
                response = packet(seq_num=1, payload="ACK")
                self.channel.udt_send(response)
                self.ReceiverAPP.deliver_data(pkt.payload)
                self.state = STATE_0
                return True
            if pkt.corrupted or pkt.sequ_num == 0:
                response = packet(seq_num=1, payload="ACK")
                self.channel.udt_send(response)
            return True
        return False
