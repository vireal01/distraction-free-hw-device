import random
import config
from state.app_state import app_state
import ui.display as display 

class Screen:
    SELECT_MODE = "SelectMode"
    POMODORO = "Pomodoro"
    TIME = "Time"
    WIFI_SETTINGS = "WiFiSettings"

# Screen management functions
def show_select_mode(oled, menu_items, current_selection):
    oled.fill(0)
    oled.text("Select Mode", 0, 0)
    for i, item in enumerate(menu_items):
        if i == current_selection:
            oled.text("-> " + item, 0, 10 + i * 10)
        else:
            oled.text("   " + item, 0, 10 + i * 10)
    oled.show()

def show_pomodoro(oled, force_update=False):
    """
    Display the pomodoro screen
    force_update: Force screen update even if content hasn't changed
    """
    oled.fill(0)
    oled.text("Pomodoro", 0, 0)
    
    if not app_state.pomodoro.is_running:
        oled.text(f"Set: {app_state.pomodoro.time} min", 0, 20)
        oled.text("Press OK to start", 0, 40)
    else:
        remaining = app_state.pomodoro.remaining_time
        minutes = remaining // 60
        seconds = remaining % 60
        oled.text(f"{minutes:02d}:{seconds:02d}", 40, 20)
        if app_state.pomodoro.is_paused:
            oled.text("Paused", 0, 35)
        else:
            oled.text("Press = pause", 0, 35)
        oled.text("Hold = resert", 0, 50)
    
    # Only show if forced or content changed
    if force_update:
        oled.show()

def show_time():
    display.show_screen_saver(random.choice(range(1, 7)))

def show_wifi_settings(oled):
    oled.fill(0)
    oled.text("WiFi Settings", 0, 0)
    oled.text("SSID: " + config.SSID, 0, 10)