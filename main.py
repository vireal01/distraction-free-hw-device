# main.py

import time
from machine import Pin
from ui.screens import Screen
import config
from services.service_container import ServiceContainer

# Initialize services
services = ServiceContainer()
services.initialize()

# Menu settings
menu_items = [Screen.POMODORO, Screen.SCREEN_SAVER, Screen.SETTINGS]
current_selection = 0

# Current screen state
current_screen = Screen.SELECT_MODE

last_irq_time = 0
DEBOUNCE_MS = 100

def on_input_state_change(screen, selection):
    global current_screen, current_selection
    current_screen = screen
    current_selection = selection
    
    # Update display based on new state
    if screen == Screen.SELECT_MODE:
        services.display.show_menu(services.input_service.menu_items, selection)
    elif screen == Screen.POMODORO:
        services.display.show_pomodoro(force_update=True)
    elif screen == Screen.SCREEN_SAVER:
        services.display.show_time()

# Register button handle callbacks
services.input_service.set_state_change_callback(on_input_state_change)

def on_encoder_state_change(screen, selection):
    global current_screen, current_selection
    current_screen = screen
    current_selection = selection
    
    # Update display based on new state
    if screen == Screen.SELECT_MODE:
        services.display.show_menu(services.encoder_service.menu_items, selection)
    elif screen == Screen.POMODORO:
        services.display.show_pomodoro(force_update=True)
    elif screen == Screen.SCREEN_SAVER:
        services.display.show_time()

# Connect callback
services.encoder_service.set_state_change_callback(on_encoder_state_change)

# Make sure the encoder knows the initial screen state
services.encoder_service.set_current_screen(current_screen, current_selection)

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
    elif current_screen == Screen.SCREEN_SAVER:
        if time_diff >= config.screen_update_interval:
            services.display.show_time()
            last_update = current_time

    time.sleep(0.1)
