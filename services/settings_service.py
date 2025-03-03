from .interfaces import SettingsServiceInterface

class SettingsService(SettingsServiceInterface):
    def __init__(self):
        self._settings = {
            'dnd_enabled': True,
            'screen_brightness': 128
        }
    
    def get_dnd_enabled(self) -> bool:
        return self._settings['dnd_enabled']
    
    def set_dnd_enabled(self, enabled: bool):
        self._settings['dnd_enabled'] = enabled