import pygame
from cell import Cell
import numpy as np

pygame.init()

boardwidth, boardheight = 800, 800
width, height = boardwidth, boardheight+200
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 25)
grey = (125, 125, 125)
border_size = 10
cells_per_row = 79 # should go into "boardwidth-10" nicely...
cell_size = -1
buffer = 1
autospeed = 100 # in ms

screen = pygame.display.set_mode((width, height))
screen.fill(white)

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

def makeNextCells(old_cells):
    next_cells = [None]*len(old_cells)

    for i in range(len(old_cells)):
        ncol = [None]*len(old_cells)
        for j in range(len(old_cells[0])):
            template_cell = old_cells[i][j]
            ncell = Cell(template_cell.x, template_cell.y, template_cell.index, template_cell.size, template_cell.state)
            ncol[j] = ncell
        next_cells[i] = ncol
    
    return next_cells

def updateCells(oldcells, newcells):
    for col in newcells:
        for c in col:
            c.update(oldcells)

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

def printBoard(cell_list):
    print(np.matrix(cell_list))
    print("\n")

def renderText(msg, font, fontsize, color, bgcolor, x, y, scrn):
    font = pygame.font.SysFont(font, fontsize, bold=True)
    helptext = font.render(msg, False, color, bgcolor)
    helptextrect = helptext.get_rect()
    helptextrect.center = (x, y)
    scrn.blit(helptext, helptextrect)

# make board
board = pygame.Surface((boardwidth - border_size + buffer, boardheight - border_size + buffer)).convert()
board_rect = board.get_rect()
board.fill(black)

# make cells
cells = createCells(board_rect, cells_per_row, buffer, 0)

# initial render
cell_rects = [[None]*cells_per_row for i in range(cells_per_row)]
renderCells(board, cells, cell_rects)

# custom events
AUTO_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(AUTO_UPDATE, 0)

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
            elif event.key == pygame.K_r:
                pygame.time.set_timer(AUTO_UPDATE, autospeed)
            elif event.key == pygame.K_s:
                pygame.time.set_timer(AUTO_UPDATE, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            left_click = pygame.mouse.get_pressed()[0]
            for i in range(len(cells)):
                for j in range(len(cells[0])):
                    if cell_rects[i][j].collidepoint(pygame.mouse.get_pos()):
                        flipCell(cells, i, j)
        if event.type == AUTO_UPDATE:
            updateThisFrame = True

    # logic
    next_cells = makeNextCells(cells)

    if updateThisFrame:
        updateCells(cells, next_cells)
        updateThisFrame = False
    
    # rendering
    renderCells(board, next_cells, cell_rects)
    
    message1 = "Press SPACE to advance the simulation by 1 step."
    x1, y1 = (width // 2, height - 175)
    renderText(message1, "arial", 20, black, None, x1, y1, screen)

    message2 = "Press R to auto-run simulation."
    x2, y2 = (width // 2, height - 150)
    renderText(message2, "arial", 20, black, None, x2, y2, screen)

    message3 = "Press S to stop the auto-run."
    x3, y3 = (width // 2, height - 125)
    renderText(message3, "arial", 20, black, None, x3, y3, screen)

    screen.blit(board, (border_size//2, border_size//2))
    pygame.display.flip()

    cells[:] = next_cells[:]

pygame.quit()