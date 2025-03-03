from machine import Pin
import time
import config
from ui.screens import Screen
from .interfaces import InputServiceInterface, PomodoroServiceInterface, SettingsServiceInterface

class InputService(InputServiceInterface):
    def __init__(self, 
                 pomodoro_service: PomodoroServiceInterface,
                 settings_service: SettingsServiceInterface):
        self.pomodoro_service = pomodoro_service
        self.settings_service = settings_service
        self.menu_items = [Screen.POMODORO, Screen.TIME, Screen.SETTINGS]
        
        # Button state tracking
        self.press_start = {
            config.left_button: 0,
            config.middle_button: 0,
            config.right_button: 0
        }
        self.last_press = {
            config.left_button: 0,
            config.middle_button: 0,
            config.right_button: 0
        }

    def handle_button(self, pin_id: int, button_value: int, 
                     current_screen: str, current_selection: int = 0):
        """Handle button press and return new screen and selection state"""
        current_time = time.ticks_ms()

        if time.ticks_diff(current_time, self.last_press[pin_id]) > 100:
            # Button Pressed
            if button_value == 0:
                self.press_start[pin_id] = current_time
            
            # Button Released
            elif button_value == 1:
                press_duration = time.ticks_diff(current_time, self.press_start[pin_id])
                
                if press_duration >= config.long_press_threshold:
                    return self._handle_long_press(pin_id, current_screen)
                else:
                    return self._handle_short_press(pin_id, current_screen, current_selection)
                    
            self.last_press[pin_id] = current_time

        return current_screen, current_selection

    def _handle_long_press(self, pin_id: int, current_screen: str):
        """Handle long press events"""
        if current_screen != Screen.SELECT_MODE and pin_id == config.left_button:
            return Screen.SELECT_MODE, 0
        elif current_screen == Screen.POMODORO and pin_id == config.middle_button:
            self.pomodoro_service.reset()
        return current_screen, 0

    def _handle_short_press(self, pin_id: int, current_screen: str, 
                          current_selection: int):
        """Handle short press events"""
        if current_screen == Screen.SELECT_MODE:
            return self._handle_menu_navigation(pin_id, current_selection)
        elif current_screen == Screen.POMODORO:
            return self._handle_pomodoro_input(pin_id, current_screen)
        elif current_screen == Screen.SETTINGS:
            return self._handle_settings_input(pin_id, current_screen, current_selection)
        return current_screen, current_selection

    def _handle_menu_navigation(self, pin_id: int, current_selection: int):
        """Handle menu navigation"""
        if pin_id == config.left_button:
            return Screen.SELECT_MODE, (current_selection - 1) % len(self.menu_items)
        elif pin_id == config.right_button:
            return Screen.SELECT_MODE, (current_selection + 1) % len(self.menu_items)
        elif pin_id == config.middle_button:
            print(f"Selected: {self.menu_items[current_selection]}")
            return self.menu_items[current_selection], current_selection
        return Screen.SELECT_MODE, current_selection

    def _handle_pomodoro_input(self, pin_id: int, current_screen: str):
        print(f"click on {pin_id} detected")
        """Handle Pomodoro screen inputs"""
        if not self.pomodoro_service.is_running():
            if pin_id == config.left_button:
                self.pomodoro_service.decrease_time()
            elif pin_id == config.right_button:
                self.pomodoro_service.increase_time()
            elif pin_id == config.middle_button:
                self.pomodoro_service.start()
        else:
            if pin_id == config.middle_button:
                if self.pomodoro_service.is_paused():
                    self.pomodoro_service.resume()
                else:
                    self.pomodoro_service.pause()
        return current_screen, 0

    def _handle_settings_input(self, pin_id: int, current_screen: str, 
                             current_setting: int):
        """Handle settings screen inputs"""
        if pin_id == config.left_button:
            return current_screen, max(0, current_setting - 1)
        elif pin_id == config.right_button:
            return current_screen, min(2, current_setting + 1)
        elif pin_id == config.middle_button:
            if current_setting == 0:
                self.settings_service.toggle_dnd()
            elif current_setting == 1:
                self.settings_service.toggle_brightness()
        return current_screen, current_setting