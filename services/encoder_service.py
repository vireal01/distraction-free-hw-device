from ui.screens import Screen
from .interfaces import EncoderServiceInterface, PomodoroServiceInterface, SettingsServiceInterface
from machine import Pin
import config
import time

class EncoderService(EncoderServiceInterface):
    def __init__(self, 
                 pomodoro_service: PomodoroServiceInterface,
                 settings_service: SettingsServiceInterface):
        self.pomodoro_service = pomodoro_service
        self.settings_service = settings_service
        self.menu_items = [Screen.POMODORO, Screen.SCREEN_SAVER, Screen.SETTINGS]
        
        # State tracking
        self.current_screen = Screen.POMODORO
        self.current_selection = 0
        
        # Debounce settings
        self.last_irq_time = 0
        self.DEBOUNCE_MS = 100  # Lower debounce for rotary encoder
        
        # Encoder state tracking
        self.last_clk_state = None
        
        # Set up encoder hardware
        self._init_hardware()
        
        # State change callback - defaults to no-op
        self.on_state_change = lambda screen, selection: None
    
    def _init_hardware(self):
        """Initialize encoder hardware and set up interrupts"""
        # Create pin objects
        self.pin_clk = Pin(config.encoder_pin_click, Pin.IN, Pin.PULL_UP)
        self.pin_dt = Pin(config.encoder_pin_dt, Pin.IN, Pin.PULL_UP)
        
        # Store initial state
        self.last_clk_state = self.pin_clk.value()
        
        # Set up interrupt for CLK pin (triggers on both rising and falling edges)
        self.pin_clk.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, 
                        handler=self._encoder_rotation_handler)
        
        # Set up button pin if available
        if hasattr(config, 'encoder_pin_sw'):
            self.pin_sw = Pin(config.encoder_pin_sw, Pin.IN, Pin.PULL_UP)
            self.pin_sw.irq(trigger=Pin.IRQ_FALLING, 
                         handler=self._encoder_button_handler)
    
    def _encoder_rotation_handler(self, pin):
        """Handle rotation detection using the two encoder pins"""
        # Debounce
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_irq_time) < self.DEBOUNCE_MS:
            return  # Ignore interrupt if within debounce period
        
        # Read current pin states
        clk_state = self.pin_clk.value()
        dt_state = self.pin_dt.value()
        
        # Check if this is a valid edge (CLK state changed)
        if clk_state != self.last_clk_state:
            # When CLK changes, if DT differs from CLK, it's rotating one way;
            # if DT is the same as CLK, it's rotating the other way
            if dt_state != clk_state:
                # Clockwise rotation (typically)
                delta = 1
                print("Rotate right")
            else:
                # Counter-clockwise rotation (typically)
                delta = -1
                print("Rotate left")
            
            # Handle the rotation based on current screen
            # For debugging
            print(f"Before rotation: screen={self.current_screen}, selection={self.current_selection}")
            
            # Handle the rotation based on current screen
            new_screen, new_selection = self.handle_rotation(delta, self.current_screen, self.current_selection)
            
            # For debugging
            print(f"After rotation: new_screen={new_screen}, new_selection={new_selection}")
            
            # Only update selection for rotations, don't change screen
            if new_selection is not None and new_selection != self.current_selection:
                self.current_selection = new_selection
                # Only notify of selection changes from rotation
                self.on_state_change(self.current_screen, self.current_selection)
        
        # Update last state and debounce time
        self.last_clk_state = clk_state
        self.last_irq_time = current_time
    
    def _encoder_button_handler(self, pin):
        """Handle button press events"""
        # Debounce
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_irq_time) < self.DEBOUNCE_MS * 2:  # Longer debounce for button
            return  # Ignore interrupt if within debounce period
        
        print("Encoder button pressed!")
        
        # Only process falling edge (button press, not release)
        if pin.value() == 0:  # Button is pressed (active low)
            # Handle button press based on current screen
            new_screen, new_selection = self.handle_button_press(self.current_screen, self.current_selection)
            
            # Update state if changed
            changed = False
            if new_screen is not None and new_screen != self.current_screen:
                self.current_screen = new_screen
                changed = True
            if new_selection is not None and new_selection != self.current_selection:
                self.current_selection = new_selection
                changed = True
                
            # Notify if state changed
            if changed:
                self.on_state_change(self.current_screen, self.current_selection)
        
        self.last_irq_time = current_time
    
    def handle_rotation(self, delta, current_screen, current_selection=0):
        """
        Handle encoder rotation based on current screen
        Returns tuple of (new_screen, new_selection)
        """
        print(f"Handling rotation: delta={delta}, screen={current_screen}")
        
        if current_screen == Screen.SELECT_MODE:
            # Menu navigation - wrap around the menu
            new_selection = (current_selection + delta) % len(self.menu_items)
            print(f"SELECT_MODE: new selection = {new_selection}")
            return None, new_selection
            
        elif current_screen == Screen.POMODORO:
            # Adjust pomodoro time if not running
            if not self.pomodoro_service.is_running():
                if delta > 0:
                    self.pomodoro_service.increase_time()
                    print("Increased pomodoro time")
                else:
                    self.pomodoro_service.decrease_time()
                    print("Decreased pomodoro time")
            return None, current_selection  # Selection doesn't change, screen doesn't change
            
        elif current_screen == Screen.SETTINGS:
            # Navigate settings
            num_settings = 3  # Adjust to your actual number of settings
            new_selection = max(0, min(current_selection + delta, num_settings - 1))
            print(f"SETTINGS: new selection = {new_selection}")
            return None, new_selection
            
        # Default - no change to screen or selection
        return None, current_selection
    
    def handle_button_press(self, current_screen, current_selection):
        """
        Handle encoder button press based on current screen
        Returns (new_screen, new_selection) tuple or (None, None) if no change
        """
        if current_screen == Screen.SELECT_MODE:
            # Select the current menu item
            return self.menu_items[current_selection], 0
            
        elif current_screen == Screen.POMODORO:
            # Start/pause the pomodoro
            if not self.pomodoro_service.is_running():
                self.pomodoro_service.start()
            else:
                if self.pomodoro_service.is_paused():
                    self.pomodoro_service.resume()
                else:
                    self.pomodoro_service.pause()
            return None, None  # No navigation change
            
        elif current_screen == Screen.SETTINGS:
            # Toggle the current setting
            if current_selection == 0:
                self.settings_service.toggle_dnd()
            elif current_selection == 1:
                self.settings_service.toggle_brightness()
            # Add more settings as needed
            return None, None  # No navigation change
            
        return None, None  # Default - no change
    
    def set_state_change_callback(self, callback):
        """Set callback for state changes"""
        self.on_state_change = callback
    
    def set_current_screen(self, screen, selection=0):
        """Update the current screen and selection"""
        self.current_screen = screen
        self.current_selection = selection