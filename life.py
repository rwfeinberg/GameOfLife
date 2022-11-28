import pygame
from cell import Cell

pygame.init()

width, height = 400, 400
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 25)
grey = (125, 125, 125)
border_size = 10
cells_per_row = 10
cell_size = -1
buffer = 1

screen = pygame.display.set_mode((width, height))
screen.fill(white)

clock = pygame.time.Clock()

pygame.display.set_caption("Game of Life")

def createCells(brect, cpr, bffr, init_state):
    csize = (brect.size[0] - bffr*cpr) / (cpr)
    arr = [None]*cpr
    x = brect.x + bffr
    y = brect.y + bffr
    for i in range(len(arr)):
        col = [None]*cpr
        for j in range(len(col)):
            cell = Cell(x, y, (i, j), (csize, csize), init_state)
            col[j] = cell
            x += csize + bffr
        x = bffr
        arr[i] = col
        y += csize + bffr
    
    return arr

def updateCells(oldcells, newcells):
    for i in range(len(newcells)):
        for j in range(len(newcells[0])):
            newcells[i][j].update(oldcells)

def renderCells(cell_board, cells, cellrects):
    for i in range(len(cells)):
        for j in range(len(cells[0])):
            c = cells[i][j]
            color = yellow if c.state == 1 else grey
            cr = pygame.draw.rect(cell_board, color, pygame.Rect(c.x, c.y, c.size[0], c.size[1]))
            cellrects[i][j] = cr

def flipCell(cells, i, j):
    cell = cells[i][j]
    if cell.state == 0:
        cell.state = 1
    elif cell.state == 1:
        cell.state = 0

# make board
board = pygame.Surface((width - border_size + buffer, height - border_size + buffer)).convert()
board_rect = board.get_rect()
board.fill(black)

# make cells
cells = createCells(board_rect, cells_per_row, buffer, 0)

# initial render
cell_rects = [[None]*cells_per_row for i in range(cells_per_row)]
renderCells(board, cells, cell_rects)

running = True
updateThisFrame = False

while running:

    # event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                updateThisFrame = True
            elif event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            left_click = pygame.mouse.get_pressed()[0]
            for i in range(len(cells)):
                for j in range(len(cells[0])):
                    if cell_rects[i][j].collidepoint(pygame.mouse.get_pos()):
                        flipCell(cells, i, j)
                        #print("Cell "+str(cells[i][j]))

    
    # logic
    next_cells = list(cells)
    if updateThisFrame:
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                
        updateCells(cells, next_cells)
        updateThisFrame = False
    

    # rendering
    renderCells(board, next_cells, cell_rects)

    screen.blit(board, (border_size//2, border_size//2))
    pygame.display.flip()

    cells = next_cells

pygame.quit()