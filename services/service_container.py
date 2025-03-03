from services.settings_service import SettingsService
from services.notification_service import NotificationService
from services.pomodoro_service import PomodoroService
from services.display_service import DisplayService
from services.input_service import InputService
from services.interfaces import (
    SettingsServiceInterface,
    NotificationServiceInterface,
    PomodoroServiceInterface,
    DisplayServiceInterface,
    InputServiceInterface
)
from hardware.hardware_interfaces import DisplayInterface
from hardware.oled_sh1106 import OLED_SH1106

class ServiceContainer:
    def __init__(self):
        # Hardware
        self._display_device: DisplayInterface = None
        
        # Services
        self.settings: SettingsServiceInterface = None
        self.notifications: NotificationServiceInterface = None
        self.pomodoro: PomodoroServiceInterface = None
        self.display: DisplayServiceInterface = None
        self.input_service: InputServiceInterface = None

    def initialize(self):
        # Initialize hardware
        self._display_device = OLED_SH1106()
        
        # Initialize base services
        self.settings = SettingsService()
        
        # Initialize dependent services
        self.notifications = NotificationService(
            settings_service=self.settings
        )
        
        self.pomodoro = PomodoroService(
            notification_service=self.notifications
        )
        
        self.display = DisplayService(
            display=self._display_device,
            settings_service=self.settings,
            pomodoro_service=self.pomodoro
        )
        
        self.input_service = InputService(
            pomodoro_service=self.pomodoro,
            settings_service=self.settings
        )