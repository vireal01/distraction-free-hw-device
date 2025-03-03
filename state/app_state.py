from models.pomodoro import PomodoroState

class ApplicationState:
    def __init__(self):
        self.pomodoro = PomodoroState(25)  # default 25 minutes
        
# Create a singleton instance
app_state = ApplicationState()