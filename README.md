MicroPython OLED
================

This is a collection of drivers for handling monochrome OLED displays. There
are many versions of such drivers, and there is even a driver for the SSD1306
included in MicroPython's repository, but I decided to make my own, because I
needed something a little bit more optimized.

To conserve memory, each version of each driver is in a separate self-contained
file that you need to copy to your board. There is no inheritance and no
multiple imports -- I'm only using the build-in `framebuf` module. Of course
that means there is some repetition between the different drivers, but that's a
price I'm willing to pay. There are also no constants that would need to be
converted to bytes before sending -- I'm using raw byte strings everywhere.

To make it fast, I'm calling MicroPython's built-in functions directly, without
wrapping them into convenience functions. I'm also only allocating any memory
once, at the beginning, and then re-using those buffers for everything.

Finally, I have added some convenience functions for flipping and mirroring the
display, reversing its colors, hardware scrolling, setting contrast and
switching it off and on.

There are no drawing functions on the display object itself, they are available
on the frame buffer object, available as the `fb` attribute.

Examples
========

SH1106 I2C Example
------------------

```python
import sh1106_i2c
from machine import I2C, Pin

i2c = I2C(-1, sda=Pin(4), scl=Pin(5), freq=400000)
d = sh1106_i2c.Display(i2c)
d.fb.fill(1)
d.fb.pixel(64, 32, 0)
d.update()
```

SH1106 SPI Example
------------------

```python
import sh1106_spi
from machine import SPI, Pin

spi = SPI(1, baudrate=20000000)
dc = Pin(12, Pin.OUT)
cs = Pin(15, Pin.OUT)
d = sh1106_spi.Display(spi, dc, cs)
d.fb.fill(1)
d.fb.pixel(64, 32, 0)
d.update()
```
