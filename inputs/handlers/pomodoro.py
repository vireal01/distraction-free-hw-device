import time
import config
import models.pomodoro as pomodoro

def handle_pomodoro(pinId: int, pomodoro_state: pomodoro.PomodoroState):
    if not pomodoro_state.is_running:
        if pinId == config.left_button:  # Left button - decrease time
            pomodoro_state.time = max(1, pomodoro_state.time - 5)
        elif pinId == config.right_button:  # Right button - increase time
            pomodoro_state.time = min(60, pomodoro_state.time + 5)
        elif pinId == config.middle_button:  # Middle button - start/pause timer

            pomodoro_state.is_running = True
            pomodoro_state.start_time = time.time()
            pomodoro_state.remaining_time = pomodoro_state.time * 60
    else:
        if pinId == config.middle_button:  # Middle button - stop timer
            if pomodoro_state.is_paused:
                pomodoro_state.is_paused = False
            else:
                pomodoro_state.is_paused = True

def handle_pomodoro_long_press(pomodoro_state):
    pomodoro_state.reset()