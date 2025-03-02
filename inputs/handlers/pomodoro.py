import time

def handle_pomodoro(pinId, pomodoro_state):
    if not pomodoro_state.is_running:
        if pinId == 19:  # Left button - decrease time
            pomodoro_state.time = max(1, pomodoro_state.time - 1)
        elif pinId == 5:  # Right button - increase time
            pomodoro_state.time = min(60, pomodoro_state.time + 1)
        elif pinId == 18:  # Middle button - start timer
            pomodoro_state.is_running = True
            pomodoro_state.start_time = time.time()
            pomodoro_state.remaining_time = pomodoro_state.time * 60
    else:
        if pinId == 18:  # Middle button - stop timer
            pomodoro_state.is_running = False