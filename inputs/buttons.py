from machine import Pin
import time
import config
from ui.screens import Screen
from inputs.handlers.main_menu import handle_select_mode
from inputs.handlers.pomodoro import handle_pomodoro
# Track button press times
press_start = {19: 0, 18: 0, 5: 0}  # For tracking long press start time
last_press = {19: 0, 18: 0, 5: 0}

def button_callback(pinId, button, oled, menu_items, current_selection, current_screen):
    current_time = time.ticks_ms()

    # Debounce: Ignore presses happening too fast (within 300ms)
    if time.ticks_diff(current_time, last_press[pinId]) > 100:
        # Button Pressed
        if button.value() == 0: 
            press_start[pinId] = current_time  # Record press start time

        # Button Released
        elif button.value() == 1: 
            press_duration = time.ticks_diff(current_time, press_start[pinId])
            
            if press_duration >= config.long_press_threshold:  # Long Press (≥ 1000ms)
                # Switch to SELECT_MODE if long press on left button
                if current_screen != Screen.SELECT_MODE and pinId == 19:
                    current_screen = Screen.SELECT_MODE
                # Reset Pomodoro state if long press on middle button
                elif current_screen == Screen.POMODORO and pinId == 18:
                    config.pomodoro_state.reset()

            else:
                if current_screen == Screen.SELECT_MODE:
                    current_screen, current_selection = handle_select_mode(pinId, menu_items, current_selection)
                elif current_screen == Screen.POMODORO:
                    handle_pomodoro(pinId, config.pomodoro_state)


        last_press[pinId] = current_time  # Update last press timestamp
        oled.show()

    return current_screen, current_selection
