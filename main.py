# main.py

import time
from machine import Pin
from inputs.buttons import button_callback
from ui.screens import show_select_mode, show_pomodoro, show_time, Screen
from ui.display import initialize_display
import config
from state import app_state

# Initialize display
oled = initialize_display()

# Button setup
buttons = {
    config.left_button: Pin(config.left_button, Pin.IN, Pin.PULL_UP),
    config.middle_button: Pin(config.middle_button, Pin.IN, Pin.PULL_UP),
    config.right_button: Pin(config.right_button, Pin.IN, Pin.PULL_UP),
}

# Menu settings
menu_items = [Screen.POMODORO, Screen.TIME]
current_selection = 0

# Current screen state
current_screen = Screen.SELECT_MODE

# Button callback IRQ handler
def button_irq_handler(pin, button):
    global current_screen, current_selection
    current_screen, current_selection = button_callback(pin, button, oled, menu_items, current_selection, current_screen)

# Set up interrupts for buttons
for pin, button in buttons.items():
    button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=lambda btn=button, p=pin: button_irq_handler(p, btn))

# Pomodoro timer state
last_update = time.ticks_ms()

# Main loop
while True:
    current_time = time.ticks_ms()
    time_diff = time.ticks_diff(current_time, last_update)
    
    if current_screen == Screen.SELECT_MODE:
        show_select_mode(oled, menu_items, current_selection)
    elif current_screen == Screen.POMODORO:
        # Update timer if running
        if app_state.pomodoro.is_running:
            if time_diff >= config.screen_update_interval:
                elapsed = int(time.time() - app_state.pomodoro.start_time)
                # Update remaining time if not paused
                if not app_state.pomodoro.is_paused:
                    app_state.pomodoro.remaining_time = max(0, app_state.pomodoro.time * 60 - elapsed)
                
                # Reset if timer has expired
                if app_state.pomodoro.remaining_time == 0:
                    app_state.pomodoro.is_running = False
                
                show_pomodoro(oled, force_update=True)
                last_update = current_time
        else:
            show_pomodoro(oled)
    elif current_screen == Screen.TIME:
        if time_diff >= config.screen_update_interval:
            show_time()
            last_update = current_time

    time.sleep(0.1)