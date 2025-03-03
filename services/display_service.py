import random
from services.interfaces import DisplayServiceInterface, PomodoroServiceInterface, SettingsServiceInterface
from hardware.hardware_interfaces import DisplayInterface

class DisplayService(DisplayServiceInterface):
    def __init__(self, display: DisplayInterface, pomodoro_service: PomodoroServiceInterface, settings_service: SettingsServiceInterface):
        self.display = display
        self.pomodoro_service = pomodoro_service
        self.settings_service = settings_service

    def show_menu(self, menu_items: list, current_selection: int):
        self.display.fill(0)
        self.display.text("Select Mode", 0, 0)
        for i, item in enumerate(menu_items):
            if i == current_selection:
                self.display.text("-> " + item, 0, 10 + i * 10)
            else:
                self.display.text("   " + item, 0, 10 + i * 10)
        self.display.show()

    def show_pomodoro(self, force_update: bool = False):
        print("Displaying pomodoro screen")
        """Display the pomodoro screen"""
        self.display.fill(0)
        self.display.text("Pomodoro", 0, 0)
        
        time_value = self.pomodoro_service.get_time()
        remaining = self.pomodoro_service.get_remaining_time()
        minutes = remaining // 60
        seconds = remaining % 60

        if not self.pomodoro_service.is_running():
            self.display.text(f"Set: {time_value:02d}:00", 0, 20)
            self.display.text("Press OK to start", 0, 40)
        else:
            self.display.text(f"{minutes:02d}:{seconds:02d}", 40, 20)
            if self.pomodoro_service.is_paused():
                self.display.text("Paused", 0, 35)
            else:
                self.display.text("Press = pause", 0, 35)
                self.display.show()
            
        if force_update:
            self.display.show()

    def show_settings(self, current_setting: int = 0):
        settings = [
            ("DND Mode", self.settings_service.get_dnd_enabled()),
            ("Brightness", self.settings_service.get_brightness()),
            ("WiFi", self.settings_service.get_wifi_enabled())
        ]
        
        self.display.fill(0)
        self.display.text("Settings", 0, 0)
        
        for i, (name, value) in enumerate(settings):
            prefix = "-> " if i == current_setting else "   "
            status = "ON" if value else "OFF" if isinstance(value, bool) else str(value)
            self.display.text(f"{prefix}{name}: {status}", 0, 15 + i * 10)
        
        self.display.text("Press OK to toggle", 0, 50)
        self.display.show()

    def show_time(self):
        """Show screen saver"""
        self.display.show_screen_saver(random.choice(range(1, 7)))
        self.display.show()

    def clear(self):
        """Clear display"""
        self.display.fill(0)
        self.display.show()

    def _show_screen_saver(self, pattern: int):
        # Implementation of screen saver patterns
        pass