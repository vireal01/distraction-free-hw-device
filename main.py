# main.py

import time
from machine import Pin
from ui.screens import Screen
import config
from services.service_container import ServiceContainer

# Initialize services
services = ServiceContainer()
services.initialize()

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

last_irq_time = 0
DEBOUNCE_MS = 100

# Button callback IRQ handler
def button_irq_handler(pin, button):
    global current_screen, current_selection, last_irq_time
    
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_irq_time) < DEBOUNCE_MS:
        return  # Ignore interrupt if within debounce period
    
    last_irq_time = current_time
    
    current_screen, current_selection = services.input_service.handle_button(
        pin_id=pin,
        button_value=button.value(),
        current_screen=current_screen,
        current_selection=current_selection
    )

    # # Update screen immediately if screen changed
    # if new_screen != current_screen:
    #     current_screen = new_screen
    #     current_selection = new_selection
        
        # Show initial screen state
    if current_screen == Screen.SELECT_MODE:
        services.display.show_menu(menu_items, current_selection)
    elif current_screen == Screen.POMODORO:
        services.display.show_pomodoro(force_update=True)
    elif current_screen == Screen.TIME:
        services.display.show_time()
    # else:
    #     current_screen = new_screen
    #     current_selection = new_selection

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
        services.display.show_menu(menu_items, current_selection)
    elif current_screen == Screen.POMODORO:
        # Update timer if running
        if services.pomodoro.is_running:
            if time_diff >= config.screen_update_interval:
                # Update remaining time if not paused
                services.display.show_pomodoro(force_update=True)
                services.pomodoro.update_timer()
                last_update = current_time
        # else:
        #     services.display.show_pomodoro()
    elif current_screen == Screen.TIME:
        if time_diff >= config.screen_update_interval:
            services.display.show_time()
            last_update = current_time

    time.sleep(0.1)
