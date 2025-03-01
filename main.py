from machine import Pin, I2C, Timer
import sh1106
import time

# I2C Settigs
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
print("I2C devices found:", i2c.scan())

# Display
oled_width = 128
oled_height = 64
oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c, addr=0x3C)

# Buttons
buttons = {
    19: Pin(19, Pin.IN, Pin.PULL_UP),
    18: Pin(18, Pin.IN, Pin.PULL_UP),
    5: Pin(5, Pin.IN, Pin.PULL_UP),
}

# Screens
class Screen:
    SELECT_MODE = "SelectMode"
    POMODORO = "Pomodoro"
    TIME = "Time"


last_press = {pin: 0 for pin in buttons.keys()}

menu_items = ["Item 1", "Item 2", "Item 3"]
current_selection = 0

# Button callbacks logic
def button_left_callback():
    global current_selection
    current_selection = (current_selection - 1) % len(menu_items)

def button_right_callback():
    global current_selection
    current_selection = (current_selection + 1) % len(menu_items)

def button_middle_callback():
    print(f"Selected: {menu_items[current_selection]}")
    oled.fill(0)
    oled.text(f"Selected: {menu_items[current_selection]}", 0, 0)
    oled.show()
    time.sleep(1)

def button_callback(pinId, button):
    if time.ticks_diff(time.ticks_ms(), last_press[pinId]) > 200:

        last_press[pinId] = time.ticks_ms()
        oled.fill(0) 
        if pinId == 19:
            button_left_callback()
        elif pinId == 18:
            button_middle_callback()
        elif pinId == 5:
            button_right_callback()
        else:
            print("Unknown button pressed")

        oled.show()

# Подключение прерываний
for pin, button in buttons.items():
    button.irq(trigger=Pin.IRQ_FALLING, handler=lambda btn=button, p=pin: button_callback(p, btn))

# Основной цикл меню
def show_menu():
    oled.fill(0)  # Очистить экран
    oled.text("Menu", 0, 0)
    for i, item in enumerate(menu_items):
        if i == current_selection:
            oled.text("-> " + item, 0, 10 + i * 10)  # Выделить выбранный пункт
        else:
            oled.text("   " + item, 0, 10 + i * 10)  # Остальные пункты
    oled.show()

# Основной цикл
while True:
    show_menu()
    time.sleep(0.1)
