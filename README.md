Examples
********

SH1106 I2C Example
==================

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
==================

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
