from models.pomodoro import PomodoroState

long_press_threshold = 1000  # Long press threshold in milliseconds (e.g., 1000 ms = 1 second)
default_pomodoro_time = 25  # minutes
pomodoro_state = PomodoroState(default_pomodoro_time)