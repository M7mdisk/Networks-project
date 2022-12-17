# Packet class
# Includes the following main functionalities
# - payload: the data load within the packet
# - seq_num: the packet sequence number
# - corrputed: a flag value to set whether the packet is corrupted or not (True, False)


class packet(object):
    def __init__(self, payload, seq_num):
        self.sequ_num = seq_num
        self.payload = payload
        self.corrupted = False

    def set_corrupt(self):
        self.corrupted = True
        self.payload = "@#$%"

    def __str__(self):
        return "Packet(seq_num=%d, payload=%s, corrupted=%s)" % (
            self.sequ_num,
            self.payload,
            self.corrupted,
        )
