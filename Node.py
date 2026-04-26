class Node:
    def __init__(self, f1_pos, f2_pos, dirs, parent=None):
        self.f1_x, self.f1_y = f1_pos
        self.f2_x, self.f2_y = f2_pos
        self.dirs = dirs 
        self.parent = parent
        
        self.g = 0  
        self.h = 0 
        self.f = 0  