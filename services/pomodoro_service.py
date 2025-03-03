from .interfaces import PomodoroServiceInterface, NotificationServiceInterface
from models.pomodoro import PomodoroState
import time

class PomodoroService(PomodoroServiceInterface):
    def __init__(self, notification_service: NotificationServiceInterface):
        self.state = PomodoroState()
        self.notification_service = notification_service
        self._init_state()
        
    def _init_state(self):
        """Initialize default state"""
        self.state.time = 25  # Default time
        self.state.is_running = False
        self.state.is_paused = False
        self.state.remaining_time = self.state.time * 60  # Set initial remaining time
        
    def reset(self):
        self._init_state()
        
    def get_time(self):
        return self.state.time
    
    def is_paused(self) -> bool: return self.state.is_paused
    
    def get_remaining_time(self) -> int: return self.state.remaining_time
    
    def is_running(self) -> bool: return self.state.is_running
    
    def start(self):
        self.state.is_running = True
        self.state.start_time = time.time()
        self.state.remaining_time = self.state.time * 60
        self.notification_service.notify_dnd_state(True)
    
    def stop(self):
        self.state.is_running = False
        self.notification_service.notify_dnd_state(False)
    
    def update_timer(self):
        """Update timer state"""
        if self.state.is_running and not self.state.is_paused:
            elapsed = int(time.time() - self.state.start_time)
            self.state.remaining_time = max(0, self.state.time * 60 - elapsed)
            
            if self.state.remaining_time == 0:
                self.stop()
    
    def pause(self):
        #TODO: Implement pause timer logic
        self.state.is_paused = True
        self.notification_service.notify_dnd_state(False)
    
    def resume(self): 
        self.state.is_paused = False
        self.notification_service.notify_dnd_state(True)
    
    def increase_time(self):
        self.state.time += 5
        self.state.remaining_time = self.state.time * 60
    
    def decrease_time(self):
        self.state.time = max(1, self.state.time - 5)
        self.state.remaining_time = self.state.time * 60
    
    def print_state(self):
        print(f"Time: {self.state.time}, Running: {self.state.is_running}, Paused: {self.state.is_paused}, Remaining: {self.state.remaining_time}")
    

    