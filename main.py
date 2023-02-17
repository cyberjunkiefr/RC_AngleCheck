import utime, sys, os
from machine import SoftI2C, Pin, SPI, reset
from math import asin, sin, radians, degrees, pi, atan2                                                                                                                                                                             
from button import *
from mpu6886 import MPU6886
import st7789
import tft_config_m5 as tft_config
import vga1_bold_16x32, vga1_bold_16x16, vga1_8x16, vga1_8x8  # font
import axp192
import colors
import pcf8563

btnA = Button(37)
btnB = Button(39)

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
pmu = axp192.AXP192(i2c, board=axp192.M5StickCPlus)
# print("Battery Status: {:.2f} V".format(pmu.batt_voltage()))

sensor = MPU6886(i2c, accel_sf=1, gyro_sf=1)

# definition du display
tft = tft_config.config(rotation=1)
tft.init()

menuon = True
menuon2 = False
degrees = True
filter = 0.0
senscount = 0
angleoffset = 0.0
corde = 0.0
dixieme_int = 0
un_int = 0
dix_int = 0
dixieme = False
un = False
dix = False
angle = 0.0


def handle_menu():
    global menuon, menuon2
    global degrees
    global dixieme_int, un_int, dix_int
    global dixieme, un, dix
    global corde
    if not menuon and not menuon2:
        tft.rotation(1)
        tft.fill(colors.BLUE)
        tft.text(vga1_bold_16x32, "MENU:", 0, 0, colors.YELLOW, colors.BLUE)
        tft.text(vga1_8x16, 'choisi mode:', 30, 30, colors.WHITE, colors.BLUE)
        tft.fill_rect(30, 50, 130, vga1_8x16.HEIGHT, colors.GREEN)
        tft.text(vga1_8x16, '1: Degrees', 30, 50, colors.BLUE, colors.GREEN)
        tft.fill_rect(30, 70, 100, vga1_8x16.HEIGHT, colors.GREEN)
        tft.text(vga1_8x16, '2: Millimetres', 30, 70, colors.WHITE, colors.BLUE)
        menuon = True
        degrees = True
    elif menuon and degrees:
        tft.rotation(1)
        tft.fill(colors.BLUE)
        tft.text(vga1_bold_16x32, "DEGREES:", 0, 0, colors.YELLOW, colors.BLUE)
        length = len('+00.00')
        width = tft.width() // 2 - length // 2 * vga1_bold_16x32.WIDTH
        height = (tft.height() // 2)
        tft.text(vga1_bold_16x32, '+00.00', width, height, colors.WHITE, colors.BLUE)
        menuon = False
    elif menuon and not degrees:
        tft.rotation(1)
        tft.fill(colors.BLUE)
        tft.text(vga1_bold_16x32, "RENTRE LARGEUR:", 0, 0, colors.YELLOW, colors.BLUE)
        length = len('00.0mm')
        width = tft.width() // 2 - length // 2 * vga1_bold_16x32.WIDTH
        height = (tft.height() // 2)
        tft.text(vga1_bold_16x32, f'{dix_int}', width, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, f'{un_int}', width + 16, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, '.', width + 32, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, f'{dixieme_int}', width + 48, height, colors.BLUE, colors.GREEN)
        tft.text(vga1_bold_16x32, 'mm', width + 64, height, colors.WHITE, colors.BLUE)
        menuon = False
        menuon2 = True
        dixieme = True
        un = False
        dix = False
    elif menuon2:
        tft.rotation(1)
        tft.fill(colors.BLUE)
        tft.text(vga1_bold_16x32, "MILIMETERS:", 0, 0, colors.YELLOW, colors.BLUE)
        length = len('+00.00')
        width = tft.width() // 2 - length // 2 * vga1_bold_16x32.WIDTH
        height = (tft.height() // 2)
        tft.text(vga1_bold_16x32, '+00.00', width, height, colors.WHITE, colors.BLUE)
        menuon2 = False


def btnA_wasReleased_menuon():
    global degrees
    if degrees:
        tft.fill_rect(30, 50, 130, vga1_8x16.HEIGHT, colors.BLUE)
        tft.text(vga1_8x16, '1: Degrees', 30, 50, colors.WHITE, colors.BLUE)
        tft.fill_rect(30, 70, 100, vga1_8x16.HEIGHT, colors.GREEN)
        tft.text(vga1_8x16, '2: Millimetres', 30, 70, colors.BLUE, colors.GREEN)
        degrees = False
    else:
        tft.fill_rect(30, 50, 130, vga1_8x16.HEIGHT, colors.GREEN)
        tft.text(vga1_8x16, '1: Degrees', 30, 50, colors.BLUE, colors.GREEN)
        tft.fill_rect(30, 70, 100, vga1_8x16.HEIGHT, colors.BLUE)
        tft.text(vga1_8x16, '2: Millimetres', 30, 70, colors.WHITE, colors.BLUE)
        degrees = True


def btnA_wasReleased_menuon2():
    global dixieme_int, un_int, dix_int
    global dixieme, un, dix
    global corde
    length = len('00.0mm')
    width = tft.width() // 2 - length // 2 * vga1_bold_16x32.WIDTH
    height = (tft.height() // 2)
    if dixieme:
        tft.text(vga1_bold_16x32, f'{dix_int}', width, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, f'{un_int}', width + 16, height, colors.BLUE, colors.GREEN)
        tft.text(vga1_bold_16x32, '.', width + 32, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, f'{dixieme_int}', width + 48, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, 'mm', width + 64, height, colors.WHITE, colors.BLUE)
        dixieme = False
        un = True
        dix = False
    elif un:
        tft.text(vga1_bold_16x32, f'{dix_int}', width, height, colors.BLUE, colors.GREEN)
        tft.text(vga1_bold_16x32, f'{un_int}', width + 16, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, '.', width + 32, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, f'{dixieme_int}', width + 48, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, 'mm', width + 64, height, colors.WHITE, colors.BLUE)
        dixieme = False
        un = False
        dix = True
    elif dix:
        tft.text(vga1_bold_16x32, f'{dix_int}', width, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, f'{un_int}', width + 16, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, '.', width + 32, height, colors.WHITE, colors.BLUE)
        tft.text(vga1_bold_16x32, f'{dixieme_int}', width + 48, height, colors.BLUE, colors.GREEN)
        tft.text(vga1_bold_16x32, 'mm', width + 64, height, colors.WHITE, colors.BLUE)
        dixieme = True
        un = False
        dix = False


def set_corde():
    global dixieme_int, un_int, dix_int
    global dixieme, un, dix
    global corde
    length = len('00.0mm')
    width = tft.width() // 2 - length // 2 * vga1_bold_16x32.WIDTH
    height = (tft.height() // 2)
    if dixieme:
        if dixieme_int < 9:
            dixieme_int += 1
        else:
            dixieme_int = 0
        tft.text(vga1_bold_16x32, f'{dixieme_int}', width + 48, height, colors.BLUE, colors.GREEN)
    elif un:
        if un_int < 9:
            un_int += 1
        else:
            un_int = 0
        tft.text(vga1_bold_16x32, f'{un_int}', width + 16, height, colors.BLUE, colors.GREEN)
    elif dix:
        if dix_int < 9:
            dix_int += 1
        else:
            dix_int = 0
        tft.text(vga1_bold_16x32, f'{dix_int}', width, height, colors.BLUE, colors.GREEN)
    corde = (dixieme_int * 0.1) + un_int + (dix_int * 10)


def readaccel(repeat=1000,index=0):
    accel = 0.0
    for icount in range(repeat):
        accel += sensor.acceleration[index]
    accel = accel / repeat
#     if (accel > 1):
#         accel = 1
#     if (accel < -1):
#         accel = -1
    return accel

def calc_angle():
    global filter, senscount, corde
    global angleoffset, angle
    accelx = readaccel(1000,0)
    accelz = readaccel(1000,2)
    #angle = (asin(-accelx)*180/pi) - angleoffset
    angle = -(atan2(accelx,accelz)*180/pi) - angleoffset
    milli = sin(radians(angle)) * corde
    strangle = f'{angle:+06.2f}'
    if angle == 0.0:
        strmilli = "+00.00"
    elif angle >= 90:
        strmilli = f'{corde:+06.2f}'
    elif angle <= -90:
        strmilli = f'{-corde:+06.2f}'
    else:
        strmilli = f'{milli:+06.2f}'
    length = len('+00.00')
    width = tft.width() // 2 - length // 2 * vga1_bold_16x32.WIDTH
    height = (tft.height() // 2)
    tft.fill_rect(width, height, 100, vga1_bold_16x32.HEIGHT, colors.BLUE)
    if degrees:
        tft.text(vga1_bold_16x32, strangle, width, height, colors.WHITE, colors.BLUE)
    else:
        tft.text(vga1_bold_16x32, strmilli, width, height, colors.WHITE, colors.BLUE)
    filter = 0.0
    senscount = 0


def count_calibrating():
    global sensor, angleoffset
    for icount in range(4):
        sec = 4 - icount
        str = f'Calibrating in {sec} sec...'
        tft.fill_rect(30, 50, 200, vga1_8x16.HEIGHT, colors.BLUE)
        tft.text(vga1_8x16, str, 30, 50, colors.GREEN, colors.BLUE)
        utime.sleep(1)
    tft.fill_rect(30, 50, 200, vga1_8x16.HEIGHT, colors.BLUE)
    accelx = readaccel(1000,0)
    accelz = readaccel(1000,2)
    angleoffset = -(atan2(accelx,accelz)*180/pi)
    
    
    


if __name__ == '__main__':
    try:
        print('Program started...')
        handle_menu()
        icount = 0
        while True:
            if btnA.wasReleased():
                if menuon:
                    btnA_wasReleased_menuon()
                elif menuon2:
                    btnA_wasReleased_menuon2()
            elif btnA.pressedFor(2.0):
                handle_menu()
                while not btnA.wasReleased():
                    utime.sleep(0.1)
            elif btnB.wasReleased() and menuon2:
                set_corde()
            elif btnB.pressedFor(2.0) and not menuon and not menuon2:
                count_calibrating()
            elif not menuon and not menuon2:
                calc_angle()

            utime.sleep(0.1)
    except KeyboardInterrupt:
        try:
            reset()
        except:
            print("Reset didn't work!!")
