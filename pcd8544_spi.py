import framebuf
import time


class Display:
    width = 84
    height = 48
    _command = bytearray((0x40, 0x80))

    def __init__(self, spi, dc, rst=None, cs=None):
        self._spi = spi
        self._cs = cs or (lambda x: x)
        self._rst = rst or (lambda x: x)
        self._dc = dc
        self._fn = bytearray([0x20])
        buffer = bytearray(504)
        self.fb = framebuf.FrameBuffer(buffer, 84, 48, framebuf.MVLSB)
        self._buffer = memoryview(buffer)

        self.reset()
        self.contrast()

    def _write(self, data, command=True):
        self._dc(not command)
        self._cs(0)
        self._spi.write(data)
        self._cs(1)

    def reset(self):
        self._rst(0)
        time.sleep_us(100)
        self._rst(1)

    def active(self, val):
        if val:
            self._fn[0] &= ~0x04
        else:
            self._fn[0] |= 0x04
        self._write(self._fn)

    def inverse(self, val):
        self._write(b'\x0d' if val else b'\x0c')

    def contrast(self, val=63, bias=20, temp=6):
        if not (0 <= val <= 127 and 16 <= bias <= 23 and 4 <= temp <= 7):
            raise ValueError()
        for c in (self._fn[0] | 0x01, temp, bias, 0x80 | val, self._fn[0]):
            self._write(bytes((c,)))

    def update(self):
        self._cs(0)
        index = 0
        for page in range(6):
            self._command[0] = 0x40 | page
            self._dc(0)
            self._spi.write(self._command)
            self._dc(1)
            self._spi.write(self._buffer[index:index + 84])
            index += self.width
        self._cs(1)
