import framebuf


class Display:
    _byte = bytearray(1)
    _word = bytearray(2)

    def __init__(self, spi, dc, cs=None, width=128, height=64):
        self._spi = spi
        self._cs = cs or (lambda x: x)
        self._dc = dc
        self.width = width
        self.height = height
        pages = height // 8
        buffer = bytearray(width * pages)
        self.fb = framebuf.FrameBuffer(buffer, width, height, framebuf.MVLSB)
        self._buffer = memoryview(buffer)
        self._move = bytearray(b'\xb0\x04\x10')
        self.reset()
        self.mirror(0)
        self.active(1)

    def _command(self, data):
        self._dc(0)
        self._cs(0)
        self._spi.write(data)
        self._cs(1)

    def reset(self):
        self._command(b'\xe2\x2f')

    def active(self, val):
        self._command(b'\xaf' if val else b'\xae')

    def inverse(self, val):
        self._command(b'\xa7' if val else b'\xa6')

    def vscroll(self, dy):
        self._byte[0] = 0x40 | dy & 0x3f
        self._command(self._byte)

    def flip(self, val):
        self._command(b'\xc0' if val else b'\xc8')

    def mirror(self, val):
        self._command(b'\xa0' if val else b'\xa1')
        self._move[1] = 0 if val else 4

    def contrast(self, val):
        self._word[0] = 0x81
        self._word[1] = val & 0xff
        self._command(self._word)

    def update(self):
        self._cs(0)
        index = 0
        for page in range(self.height // 8):
            self._move[0] = 0xb0 | page
            self._dc(0)
            self._spi.write(self._move)
            self._dc(1)
            self._spi.write(self._buffer[index:index + self.width])
            index += self.width
        self._cs(1)
