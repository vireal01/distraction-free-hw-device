import time

class PomodoroState:
    def __init__(self):
        self.time = 25 # Default time in minutes
        self.is_running = False
        self.start_time = 0
        self.remaining_time = 0
        self.is_paused = False