import modules.sh1106 as sh1106
from machine import I2C, Pin
import framebuf
import config
from .hardware_interfaces import DisplayInterface


class OLED_SH1106(DisplayInterface): 
    """Adapter for SSD1306 OLED display implementing DisplayInterface"""

    def __init__(self, oled_width=128, oled_height=64, i2c_id=0, sda_pin=config.sda_pin, scl_pin=config.scl_pin):
        """Initialize OLED display with given parameters"""
        i2c = I2C(i2c_id, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        self._display = sh1106.SH1106_I2C(oled_width, oled_height, i2c, addr=0x3C, rotate=config.screen_rotate_degree)

    def fill(self, color: int):
        """Fill display with color (0=black, 1=white)"""
        self._display.fill(color)

    def text(self, text: str, x: int, y: int):
        """Draw text at position"""
        self._display.text(text, x, y)
        
    def blit(self, image, x, y):
        """Draw image at position"""
        self._display.blit(image, x, y)

    def show(self):
        """Update display with current buffer"""
        self._display.show()

    def clear(self):
        """Clear display"""
        self._display.fill(0)
        self._display.show()
     
    def show_screen_saver(self, index):
        self._display.fill(0)
        self._draw_bitmap_from_file(f'/assets/screen{index}.pbm', 0, 0)
        self.show()

    # Function to draw a bitmap from a file
    def _draw_bitmap_from_file(self, file_name, x, y):
        image = self._load_image(file_name)
        self.blit(image, x, y)

    def _load_image(self, filename):
        with open(filename, 'rb') as f:
            f.readline()
            f.readline()
            width, height = [int(v) for v in f.readline().split()]
            data = bytearray(f.read())
        return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)