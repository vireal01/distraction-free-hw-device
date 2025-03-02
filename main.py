# main.py

import time
from machine import Pin
from inputs.buttons import button_callback
from ui.screens import show_select_mode, show_pomodoro, show_time, Screen
from ui.display import initialize_display
import config

# Initialize display
oled = initialize_display()

# Button setup
buttons = {
    19: Pin(19, Pin.IN, Pin.PULL_UP),
    18: Pin(18, Pin.IN, Pin.PULL_UP),
    5: Pin(5, Pin.IN, Pin.PULL_UP),
}

# Menu settings
menu_items = [Screen.POMODORO, Screen.TIME]
current_selection = 0

# Current screen state
current_screen = "SelectMode"

# Button callback IRQ handler
def button_irq_handler(pin, button):
    global current_screen, current_selection
    current_screen, current_selection = button_callback(pin, button, oled, menu_items, current_selection, current_screen)

# Set up interrupts for buttons
for pin, button in buttons.items():
    button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=lambda btn=button, p=pin: button_irq_handler(p, btn))

# Main loop
while True:
    if current_screen == Screen.SELECT_MODE:
        show_select_mode(oled, menu_items, current_selection)
    elif current_screen == Screen.POMODORO:
        if config.pomodoro_state.is_running:
            elapsed = int(time.time() - config.pomodoro_state.start_time)
            config.PomodoroState = max(0, config.pomodoro_state.time * 60 - elapsed)
            
            if config.pomodoro_state.remaining_time == 0:
                config.pomodoro_state.is_running = False
        
        show_pomodoro(oled)
    elif current_screen == Screen.TIME:
        show_time(oled)

    time.sleep(0.1)
