# Simulation testing part
# This file glow together the scenario we want to test 
# using all the classes that creates the application layer, transport layer, and the unreliable channel 


import simpy
from app import SenderAPP, ReceiverAPP
from channel import channel
from rdt_2 import *



##### __START__: SETTING PARAMETER #######
env=simpy.Environment()

Sender_app = SenderAPP(env)
Receiver_app = ReceiverAPP(env)


rdt1_sender = rdt_sender(env)
rdt1_receiver= rdt_receiver(env)

data_channel = channel (env=env, corrupt_p= 0, lost_p=0, delay=2, name="DATA_channel")
ack_channel = channel( env=env, corrupt_p=0, lost_p=0, delay=2, name="ACK_channel")


##### __END__: SETTING PARAMETER #######


##### __START__: Objects Connection Setup #######

# connect upper layer (sender APP) to lower layer (sender)
Sender_app.rdt_sender = rdt1_sender		

# connect lower layer sender to the unreliable channel
rdt1_sender.channel = data_channel

# connect the channel to the receiver side 
data_channel.receiver = rdt1_receiver

# connect lower layer (receiver) to upper layer (receiver APP)
rdt1_receiver.ReceiverAPP = Receiver_app

# connect lower layer (receiver) to channel (for ACK, NAK)
rdt1_receiver.channel = ack_channel

# connect channel (ACK) to lower layer (sender)
ack_channel.receiver = rdt1_sender




#run the simulation 
env.run(until=100)