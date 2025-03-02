from machine import Pin
import modules.sh1106 as sh1106
import time
import config

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

def show_pomodoro(oled):
    oled.fill(0)
    oled.text("Pomodoro", 0, 0)
    
    if not config.pomodoro_state.is_running:
        oled.text(f"Set: {config.pomodoro_state.time} min", 0, 20)
        oled.text("Press OK to start", 0, 40)
    else:
        remaining = config.pomodoro_state.remaining_time
        minutes = remaining // 60
        seconds = remaining % 60
        oled.text(f"Time: {minutes:02d}:{seconds:02d}", 0, 20)
        oled.text("Press OK to stop", 0, 40)
    
    oled.show()

def show_time(oled):
    oled.fill(0)
    oled.text("Time", 0, 0)
    oled.text("Current time: 12:00", 0, 10)
    oled.show()

def show_wifi_settings(oled):
    oled.fill(0)
    oled.text("WiFi Settings", 0, 0)
    oled.text("SSID: " + config.SSID, 0, 10)