class Rect:
    def __init__(self, x, y, w, h):
        # Defines a rect starting at given x,y with a given height and width
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h