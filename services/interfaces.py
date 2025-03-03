class NotificationServiceInterface:
    def notify_dnd_state(self, is_active): pass
    def should_notify_dnd(self): pass

class SettingsServiceInterface:
    def get_dnd_enabled(self) -> bool: pass
    def set_dnd_enabled(self, enabled: bool): pass
    def get_brightness(self) -> int: pass
    def set_brightness(self, value: int): pass
    
class PomodoroServiceInterface:
    def start(self): pass
    def stop(self): pass
    def pause(self): pass
    def resume(self): pass
    def increase_time(self): pass
    def decrease_time(self): pass
    def get_time(self) -> int: pass
    def is_running(self) -> bool: pass
    def is_paused(self) -> bool: pass
    def get_remaining_time(self) -> int: pass
    def reset(self): pass
    def print_state(self): pass

class DisplayServiceInterface:
    """High-level display service interface for screen rendering"""
    def show_menu(self, menu_items: list, current_selection: int):
        """Show menu screen with selection
        
        Args:
            menu_items: List of available menu options
            current_selection: Currently selected menu item index
        """
        pass

    def show_pomodoro(self, force_update: bool = False):
        """Show pomodoro timer screen
        
        Args:
            force_update: Force display update regardless of state
        """
        pass

    def show_settings(self, current_setting: int = 0):
        """Show settings screen
        
        Args:
            current_setting: Currently selected setting index
        """
        pass

    def show_time(self):
        """Show time/screensaver screen"""
        pass

    def clear(self):
        """Clear display content"""
        pass


# TODO: The interface is not complete
class InputServiceInterface:
    def handle_button(self, pin_id: int, button_value: int, 
                     current_screen: str, current_selection: int = 0):
        """Public method for handling button events"""
        pass