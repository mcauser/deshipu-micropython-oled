import framebuf


class Display:
    _byte = bytearray(1)
    _word = bytearray(2)

    def __init__(self, i2c, address=0x3c, width=128, height=64):
        self._i2c = i2c
        self._address = address
        self.width = width
        self.height = height
        pages = height // 8

        self._command = bytearray(b'\x21\x00\x7f\x22\x00\x0f')
        self._command[2] = width - 1
        if width == 64:
            self._command[1] += 32
            self._command[2] += 32
        self._command[5] = pages - 1
        self._i2c.writeto_mem(self._address, 0x00, b'\xae\x20\x00\x40\x00\xa1'
                              b'\xc8\xd3\x00\xd5\x80\xd9\xf1\xdb\x30\x8d\x14'
                              b'\x81\xff\xa4\xa6')
        self._word[0] = 0xa8
        self._word[1] = height - 1
        self._i2c.writeto_mem(self._address, 0x00, self._word)
        self._word[0] = 0xda
        self._word[1] = 0x02 if height == 32 else 0x12
        self._i2c.writeto_mem(self._address, 0x00, self._word)
        self.active(True)

        buffer = bytearray(width * pages)
        self.fb = framebuf.FrameBuffer(buffer, width, height, framebuf.MVLSB)
        self._buffer = buffer

    def active(self, val):
        self._i2c.writeto_mem(self._address, 0x00, b'\xaf' if val else b'\xae')

    def inverse(self, val):
        self._i2c.writeto_mem(self._address, 0x00, b'\xa7' if val else b'\xa6')

    def vscroll(self, dy):
        self._byte[0] = 0x40 | dy & 0x3f
        self._i2c.writeto_mem(self._address, 0x00, self._byte)

    def flip(self, val):
        self._i2c.writeto_mem(self._address, 0x00, b'\xc0' if val else b'\xc8')

    def mirror(self, val):
        self._i2c.writeto_mem(self._address, 0x00, b'\xa0' if val else b'\xa1')

    def contrast(self, val):
        self._word[0] = 0x81
        self._word[1] = val & 0xff
        self._i2c.writeto_mem(self._address, 0x00, self._word)

    def update(self):
        self._i2c.writeto_mem(self._address, 0x00, self._command)
        self._i2c.writeto_mem(self._address, 0x40, self._buffer)
