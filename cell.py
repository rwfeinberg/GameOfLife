import pygame

class Cell():
    def __init__(self, x, y, index, size, state):
        self.state = state
        self.index = index
        self.x = x
        self.y = y
        self.size = size
    
    def __str__(self):
        return str(self.state)
        
    
    def __repr__(self):
        return str(self.state)
    
    # update self.state accordingly
    def update(self, cells):
        i, j = self.index
        max = len(cells) - 1

        # check if edge cell
        if (i == 0 or j == 0 or i == max or j == max):
            #print("Cell "+str(self.index)+" is on an edge")
            return
        

        # scan neighbors
        sum = 0
        for a in range(i-1, i+2):
            for b in range(j-1, j+2):
                sum += cells[a][b].state
        sum -= cells[i][j].state

        # update state
        if ((self.state == 0) and (sum == 3)):
            self.state = 1
        elif ((self.state == 1) and (sum < 2)):
            self.state = 0
        elif ((self.state == 1) and (sum > 3)):
            self.state = 0
