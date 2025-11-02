from Chat_Memory import short_memory


class Convo_manager():
    def __init__(self):
        self.isTalking = False
        self.inConvo = False

    
    def toggle_talking(self):
        self.isTalking = not self.isTalking