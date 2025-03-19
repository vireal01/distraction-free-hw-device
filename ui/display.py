import modules.sh1106 as sh1106
from machine import I2C, Pin
import framebuf
import config

# I2C Setup for Display
i2c = I2C(0, scl=Pin(config.scl_pin), sda=Pin(config.sda_pin), freq=400000)
oled_width = 128
oled_height = 64
oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c, addr=0x3C, rotate=config.screen_rotate_degree)

def initialize_display():
    print("I2C devices found:", i2c.scan())
    return oled

def show_wifi_status(wlan, isConnecting=False):
    oled.fill(0)
    if wlan.isconnected():
        oled.text("Connected!", 0, 0)
        oled.text("IP: " + wlan.ifconfig()[0], 0, 10)
    elif isConnecting:
        oled.text("Connecting to WiFi...", 0, 0)
    else:
        oled.text("Not connected", 0, 0)
    oled.show()

def show_welcome_screen():
    oled.fill(0)
    draw_bitmap_from_file('/assets/hello.pbm', 0, 0)
    oled.show()

def show_happy_screen(index):
    oled.fill(0)
    print(f'/assets/happy{index%2}.pbm')
    draw_bitmap_from_file(f'/assets/happy{index%2}.pbm', 0, 0)
    oled.show()

def show_screen_saver(index):
    oled.fill(0)
    draw_bitmap_from_file(f'/assets/screen{index}.pbm', 0, 0)
    oled.show()

# Function to draw a bitmap from a file
def draw_bitmap_from_file(file_name, x, y):
    image = load_image(file_name)
    oled.blit(image, x, y)

def load_image(filename):
    with open(filename, 'rb') as f:
        f.readline()
        f.readline()
        width, height = [int(v) for v in f.readline().split()]
        data = bytearray(f.read())
    return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)