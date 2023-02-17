"""Generic ESP32_S2 with ST7789 240x320 display"""

from machine import Pin, SPI
import st7789

TFA = 0
BFA = 0

def config(rotation=0, buffer_size=0, options=0):
    return st7789.ST7789(
        SPI(1, baudrate=20_000_000, sck=Pin(13,Pin.OUT), miso=Pin(4,Pin.IN),mosi=Pin(15,Pin.OUT)),
        135,
        240,
        reset=Pin(18, Pin.OUT),
        cs=Pin(5, Pin.OUT),
        dc=Pin(23, Pin.OUT),
        #backlight=Pin(33, Pin.OUT),
        rotation=rotation,
        options=options,
        buffer_size=buffer_size)