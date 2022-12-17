# a quick test to see the if packet class works

from packet import packet

test_1 = packet(seq_num=1, payload="Testing packet 1")
print(test_1)

test_2 = packet(seq_num=20, payload="Testing packet 20")
print(test_2)
test_2.set_corrupt()

print(test_2)
