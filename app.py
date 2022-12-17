# Application layer simulation consists of two parts (sender, and receiver)
#
# The Sender APP:
# - create new message
# - call transport layer rdt_sender to deliver messages through rd_send()


# The Receiver APP:
# - recieve message from the transport layer through deliver_data()
# - validate the information recieved


import simpy
import random
import packet
import sys


class SenderAPP(object):
    def __init__(self, env):
        self.env = env
        self.rdt_sender = None
        self.total_messages = 0

        self.env.process(self.app_process())

    def app_process(self):

        while True:
            # set a random timer to send messages within that selected simulation time
            time = random.randint(3, 4)
            yield self.env.timeout(time)

            # generate a message and send it to the lower layer
            message = "hello " + str(self.total_messages)
            print(
                "TIME: ",
                self.env.now,
                "SenderAPP: Attempting Sending message:",
                message,
            )
            if self.rdt_sender.rdt_send(message):
                # this means the message has been successfully processed by the lower layer
                self.total_messages += 1
                print(
                    "TIME: ",
                    self.env.now,
                    "SenderAPP: Message sent successfully:",
                    message,
                )
            else:
                print(
                    "TIME: ",
                    self.env.now,
                    "SenderAPP: Failed to send message:",
                    message,
                )


class ReceiverAPP(object):
    def __init__(self, env):
        self.env = env
        self.total_rec_messages = 0

    def deliver_data(self, data):
        # This method is the middle-man between the application layer and the transport layer
        # to handle incoming packets
        # responsible of validating the information received
        # for the purpose of this example: we will validate by checking if this is all lowercase message
        print("Time: ", self.env.now, "ReceiverAPP: Received data message ", data)

        if not (data.islower()):
            print("ERORR!!!!!!")
            print("Stop simulation......")
            sys.exit(0)

        # otherwise we increment the number of received data
        self.total_rec_messages += 1
