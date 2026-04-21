class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        g = 0
        h = 0
        f = g + h
        parent = None
        
