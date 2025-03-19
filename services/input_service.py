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
        self.menu_items = [Screen.POMODORO, Screen.SCREEN_SAVER, Screen.SETTINGS]
        
        # Button state tracking
        self.press_start = {
            config.first_button: 0,
            config.second_button: 0,
            config.third_button: 0,
            config.fourth_button: 0, # Shift button
        }
        self.last_press = {
            config.first_button: 0,
            config.second_button: 0,
            config.third_button: 0,
            config.fourth_button: 0  # Shift button
        }
        
        self.is_shift_active = False
       
       
        self.current_screen = Screen.POMODORO
        self.current_selection = 0
        
        # Initialize button action mappings
        self._init_action_mappings()
        self._init_hardware()
   
    def _init_hardware(self):
        """Initialize input hardware and set up interrupts"""
        # Button setup
        self.buttons = {
            config.first_button: Pin(config.first_button, Pin.IN, Pin.PULL_UP),
            config.second_button: Pin(config.second_button, Pin.IN, Pin.PULL_UP),
            config.third_button: Pin(config.third_button, Pin.IN, Pin.PULL_UP),
            config.fourth_button: Pin(config.fourth_button, Pin.IN, Pin.PULL_UP),
        }
        
        # Set up interrupts for buttons
        for pin_id, button in self.buttons.items():
            button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, 
                    handler=lambda btn=button, p=pin_id: self._button_irq_handler(p, btn))
                    
        # Last IRQ time for debouncing
        self.last_irq_time = 0
        self.DEBOUNCE_MS = 100
    
    def _button_irq_handler(self, pin_id, button):
        """Interrupt handler for button presses"""
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_irq_time) < self.DEBOUNCE_MS:
            return  # Ignore interrupt if within debounce period
        
        self.last_irq_time = current_time
        
        new_screen, new_selection = self.handle_button(
            pin_id=pin_id,
            button_value=button.value(),
            current_screen=self.current_screen,
            current_selection=self.current_selection
        )
        
        # Update current state
        if new_screen is not None:
            self.current_screen = new_screen
        if new_selection is not None:
            self.current_selection = new_selection
            
        # Notify application of state change (could use a callback or event)
        self.on_state_change(self.current_screen, self.current_selection)
    
    def on_state_change(self, screen, selection):
        """Called when input causes state change - override this or set a callback"""
        pass
    
    def set_state_change_callback(self, callback):
        """Set callback for state changes"""
        self.on_state_change = callback
    
    
    def _init_action_mappings(self):
        """Initialize all button action mappings for different screens and shift states"""
        # Action mapping structure: {screen: {shift_state: {button: action_function}}}
        self.action_map = {
            # SELECT_MODE screen actions
            Screen.SELECT_MODE: {
                # Normal mode (shift not pressed)
                False: {
                    config.first_button: self._menu_up,
                    config.second_button: self._menu_select,
                    config.third_button: self._menu_down,
                },
                # Shift mode (shift pressed)
                True: {
                    config.first_button: self._menu_home,
                    config.second_button: self._menu_back,
                    config.third_button: self._menu_end,
                }
            },
            
            # POMODORO screen actions
            Screen.POMODORO: {
                # Normal mode
                False: {
                    config.first_button: self._pomodoro_decrease_time,
                    config.second_button: self._pomodoro_start_pause_resume,
                    config.third_button: self._pomodoro_increase_time,
                },
                # Shift mode
                True: {
                    config.first_button: self._pomodoro_exit_screen,
                    config.second_button: self._pomodoro_reset_timer, # TODO: And new features
                    config.third_button: lambda current_screen, current_selection: (current_screen, current_selection), # Empty placeholder
                }
            },
            
            # SETTINGS screen actions
            Screen.SETTINGS: {
                # Normal mode
                False: {
                    config.first_button: self._settings_prev,
                    config.second_button: self._settings_toggle,
                    config.third_button: self._settings_next,
                },
                # Shift mode
                True: {
                    config.first_button: self._exit_settings,
                    config.second_button: self._exit_settings,
                    config.third_button: self._exit_settings,
                }
            },
            
            # SCREEN_SAVER actions
            Screen.SCREEN_SAVER: {
                # Any button in any mode exits screen saver
                False: {
                    config.first_button: (),
                    config.second_button: (),
                    config.third_button: (),
                },
                True: {
                    config.first_button: self._exit_screensaver,
                    config.second_button: self._exit_screensaver,
                    config.third_button: self._exit_screensaver,
                }
            }
        }
        
        # Long press action map (separate from short press)
        self.long_press_actions = {
            config.first_button: self._goto_menu,
            config.second_button: lambda *args: (None, None),  # No default action
            config.third_button: lambda *args: (None, None),  # No default action
            config.fourth_button: lambda *args: (None, None)  # No default action
        }
    
    def handle_button(self, pin_id: int, button_value: int, 
                     current_screen: str, current_selection: int = 0):
        """Handle button press and return new screen and selection state"""
        current_time = time.ticks_ms()

        # Debounce
        if time.ticks_diff(current_time, self.last_press[pin_id]) > 100:
            # Button Pressed
            if button_value == 0:
                if pin_id == config.fourth_button:
                    self.is_shift_active = True
                self.press_start[pin_id] = current_time
            
            # Button Released
            elif button_value == 1:
                # Skip processing for shift button release
                if pin_id == config.fourth_button:
                    self.press_start[pin_id] = 0
                    self.last_press[pin_id] = current_time
                    self.is_shift_active = False
                    return current_screen, current_selection
                
                press_duration = time.ticks_diff(current_time, self.press_start[pin_id])
                
                if press_duration >= config.long_press_threshold:
                    result = self._handle_long_press(pin_id, current_screen, current_selection)
                else:
                    result = self._handle_short_press(pin_id, current_screen, current_selection)
                
                # Reset button press start time
                self.press_start[pin_id] = 0
                
                # If result has actual values, return them
                if result and result[0] is not None:
                    return result
                    
            self.last_press[pin_id] = current_time

        return current_screen, current_selection

    def _handle_long_press(self, pin_id: int, current_screen: str, current_selection: int):
        """Handle long press events using the action map"""
        if pin_id in self.long_press_actions:
            return self.long_press_actions[pin_id](current_screen, current_selection)
        return current_screen, current_selection

    def _handle_short_press(self, pin_id: int, current_screen: str, 
                          current_selection: int):
        """Handle short press events using the action map"""
        
        print(f"shift active ${self.is_shift_active} and pressing ${pin_id}")
        
        # Check if we have an action map for this screen
        if current_screen in self.action_map:
            # Check if we have actions for this shift state
            if self.is_shift_active in self.action_map[current_screen]:
                # Check if we have an action for this button
                if pin_id in self.action_map[current_screen][self.is_shift_active]:
                    # Call the action function with current state
                    action_fn = self.action_map[current_screen][self.is_shift_active][pin_id]
                    return action_fn(current_screen, current_selection)
        
        # Default: no change
        return current_screen, current_selection
    
    # ==========================================================================
    # ACTION FUNCTIONS - Each returns (new_screen, new_selection)
    # ==========================================================================
    
    # ---------- Long Press Actions ----------
    def _goto_menu(self, current_screen: str, current_selection: int):
        """Long press action to go to menu"""
        if current_screen != Screen.SELECT_MODE:
            return Screen.SELECT_MODE, 0
        return current_screen, current_selection
    
    def _reset_current(self, current_screen: str, current_selection: int):
        """Long press action to reset current screen state"""
        if current_screen == Screen.POMODORO:
            self.pomodoro_service.reset()
        return current_screen, current_selection
    
    # ---------- Menu Navigation Actions ----------
    def _menu_up(self, current_screen: str, current_selection: int):
        """Move menu selection up"""
        return Screen.SELECT_MODE, (current_selection - 1) % len(self.menu_items)
    
    def _menu_down(self, current_screen: str, current_selection: int):
        """Move menu selection down"""
        return Screen.SELECT_MODE, (current_selection + 1) % len(self.menu_items)
    
    def _menu_select(self, current_screen: str, current_selection: int):
        """Select current menu item"""
        print(f"Selected: {self.menu_items[current_selection]}")
        return self.menu_items[current_selection], current_selection
    
    def _menu_home(self, current_screen: str, current_selection: int):
        """Go to first menu item (with shift)"""
        return Screen.SELECT_MODE, 0
    
    def _menu_end(self, current_screen: str, current_selection: int):
        """Go to last menu item (with shift)"""
        return Screen.SELECT_MODE, len(self.menu_items) - 1
    
    def _menu_back(self, current_screen: str, current_selection: int):
        """Go back to previous screen (with shift)"""
        # Implement your back navigation logic here
        return Screen.SELECT_MODE, 0  # Default back to pomodoro
    
    # ---------- Pomodoro Actions ----------
    def _pomodoro_decrease_time(self, current_screen: str, current_selection: int):
        """Decrease pomodoro time"""
        if not self.pomodoro_service.is_running():
            self.pomodoro_service.decrease_time()
        return current_screen, current_selection
    
    def _pomodoro_increase_time(self, current_screen: str, current_selection: int):
        """Increase pomodoro time"""
        if not self.pomodoro_service.is_running():
            self.pomodoro_service.increase_time()
        return current_screen, current_selection
    
    def _pomodoro_start_pause_resume(self, current_screen: str, current_selection: int):
        """Start, pause or resume pomodoro"""
        if not self.pomodoro_service.is_running():
            self.pomodoro_service.start()
        else:
            if self.pomodoro_service.is_paused():
                self.pomodoro_service.resume()
            else:
                self.pomodoro_service.pause()
        return current_screen, current_selection
    
    def _pomodoro_exit_screen(self, current_screen: str, current_selection: int):
        """Leave Pomodoro screen"""
        return Screen.SELECT_MODE, 0 
    
    def _pomodoro_reset_timer(self, current_screen: str, current_selection: int):
        """Reset pomodoro timer"""
        if self.pomodoro_service.is_running():
            self.pomodoro_service.reset()
        return current_screen, current_selection

    
    # ---------- Settings Actions ----------
    def _settings_prev(self, current_screen: str, current_setting: int):
        """Move to previous setting"""
        return current_screen, max(0, current_setting - 1)
    
    def _settings_next(self, current_screen: str, current_setting: int):
        """Move to next setting"""
        return current_screen, min(2, current_setting + 1)
    
    def _exit_settings(self, current_screen: str, current_selection: int):
        return Screen.POMODORO, 0  # Return to pomodoro by default
    
    def _settings_toggle(self, current_screen: str, current_setting: int):
        """Toggle current setting"""
        if current_setting == 0:
            self.settings_service.toggle_dnd()
        elif current_setting == 1:
            self.settings_service.toggle_brightness()
        return current_screen, current_setting
    
    # ---------- Screensaver Actions ----------
    def _exit_screensaver(self, current_screen: str, current_selection: int):
        """Exit screensaver mode"""
        return Screen.SELECT_MODE, 0 