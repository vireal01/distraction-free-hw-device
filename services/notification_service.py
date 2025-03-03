from .interfaces import NotificationServiceInterface
from .interfaces import SettingsServiceInterface
import urequests

class NotificationService(NotificationServiceInterface):
    def __init__(self, settings_service: SettingsServiceInterface):
        self.settings_service = settings_service
        self.tasker_url = None

    def notify_dnd_state(self, is_active):
        if not self.tasker_url or not self.should_notify_dnd():
            return
        try:
            data = {"dnd": "on" if is_active else "off"}
            response = urequests.post(self.tasker_url, json=data)
            response.close()
        except:
            print("Failed to notify Tasker")

    def should_notify_dnd(self):
        return self.settings_service.get_dnd_enabled()