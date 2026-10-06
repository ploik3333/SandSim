FrameTimers = set()

class FrameTimer:
    def __init__(self, frames):
        FrameTimers.add(self)
        self.initial = frames
        self.framesLeft = frames

    def tick(self):
        self.framesLeft -= 1

    def reset(self):
        self.framesLeft = self.initial

    def done(self):
        return self.framesLeft <= 0