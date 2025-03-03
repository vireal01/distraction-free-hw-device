class DisplayInterface:
    """Hardware display interface"""
    def fill(self, color: int): pass
    def text(self, text: str, x: int, y: int): pass
    def show(self): pass
    def clear(self): pass
    def show_screen_saver(self, index): pass
    def blit(self, image, x, y): pass