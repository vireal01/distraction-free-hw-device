class PomodoroState:
    def __init__(self, time=25):
        self.time = time
        self.is_running = False
        self.start_time = 0
        self.remaining_time = 0

    def reset(self):
        """Reset pomodoro state to default values"""
        self.is_running = False
        self.start_time = 0
        self.remaining_time = 0