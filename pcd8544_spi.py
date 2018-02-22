import framebuf
import time


class Display:
    width = 84
    height = 48

    def __init__(self, spi, dc, rst=None, cs=None):
        self._spi = spi
        self._cs = cs or (lambda x: x)
        self._rst = rst or (lambda x: x)
        self._dc = dc
        self._fn = 0x20
        buffer = bytearray(504)
        self.fb = framebuf.FrameBuffer(buffer, 84, 48, framebuf.MONO_VLSB)
        self._buffer = memoryview(buffer)

        self.reset()

    def _command(self, command):
        self._dc(0)
        self._cs(0)
        self._spi.write(command)
        self._cs(1)

    def reset(self):
        self._rst(0)
        time.sleep_us(100)
        self._rst(1)
        time.sleep_us(100)
        self.contrast()
        self.inverse(0)

    def active(self, val):
        if val:
            self._fn &= ~0x04
        else:
            self._fn |= 0x04
        self._command(bytes((self._fn,)))

    def inverse(self, val):
        self._command(b'\x0d' if val else b'\x0c')

    def contrast(self, val=63, bias=20, temp=6):
        if not (0 <= val <= 127 and 16 <= bias <= 23 and 4 <= temp <= 7):
            raise ValueError()
        self._command(bytes((self._fn | 1, temp, bias, 0x80 | val, self._fn)))

    def update(self):
        self._dc(0)
        self._cs(0)
        self._spi.write(b'\x40\x80')
        self._dc(1)
        self._spi.write(self._buffer)
        self._cs(1)
