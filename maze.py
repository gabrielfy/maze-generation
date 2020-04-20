from random import choice, randint
import pygame
import time
import math

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Define width and height of window
SIZE = 500
CELL_SIZE = 20
WINDOW_SIZE = math.ceil(SIZE / CELL_SIZE)
FPS = 30


class Cell(object):
    def __init__(self, screen, size, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.screen = screen
        self.size = size
        self.borders = [True, True, True, True] # TOP, RIGHT, BOTTOM, LEFT
        self.border_size = 2
    
    def draw(self):
        if self.visited:
            self._draw_borders()

    def highlight(self):
        self._fill(GREEN)

    def _draw_borders(self):
        row, col = self.row * self.size, self.col * self.size

        if self.borders[0]: # TOP
            self._border((row, col), (row, col + self.size))
        
        if self.borders[1]: # RIGHT
            self._border((row, col  + self.size), (row  + self.size, col  + self.size))
        
        if self.borders[2]: # BOTTOM
            self._border((row  + self.size, col), (row  + self.size, col  + self.size))

        if self.borders[3]:# LEFT
            self._border((row, col), (row  + self.size, col))

    def _border(self, start_pos, end_pos):
        pygame.draw.line(self.screen, WHITE, start_pos, end_pos, self.border_size)

    def _fill(self, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(self.row * self.size, self.col * self.size, self.size, self.size))


def has_unvisited_neighbors(maze, cell):
    neighbors = []

    if cell.row - 1 >= 0 and not maze[cell.row - 1][cell.col].visited: # TOP
        neighbors.append(maze[cell.row - 1][cell.col])
    
    if cell.col - 1 >= 0 and not maze[cell.row][cell.col - 1].visited: # RIGHT
        neighbors.append(maze[cell.row][cell.col - 1])

    if cell.row + 1 < WINDOW_SIZE and not maze[cell.row + 1][cell.col].visited: # BOTTOM
        neighbors.append(maze[cell.row + 1][cell.col])
    
    if cell.col + 1 < WINDOW_SIZE and not maze[cell.row][cell.col + 1].visited: # LEFT
        neighbors.append(maze[cell.row][cell.col + 1])
    
    return neighbors


def remove_wall(a, b):
    x = a.col - b.col
    if x == 1:
        a.borders[3] = False
        b.borders[1] = False
    elif x == -1:
        a.borders[1] = False
        b.borders[3] = False

    y = a.row - b.row
    if y == 1:
        a.borders[0] = False
        b.borders[2] = False
    elif y == -1:
        a.borders[2] = False
        b.borders[0] = False


if __name__ == '__main__':

    # Define window
    screen = pygame.display.set_mode((SIZE + 2, SIZE + 2))
    pygame.display.set_caption('Maze')
    
    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

    # Create matrix of cells
    maze = []
    for i in range(WINDOW_SIZE):
        maze.append([])
        for j in range(WINDOW_SIZE):
            maze[i].append(Cell(screen, SIZE_CELL, i, j))
    
    # Stack of cells
    stack = []

    # Start cell
    current = maze[0][0]
    current.visited = True
    stack.append(current)
    
    running = True
    while running:

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Close window
                running = False
        
        # Set background color to black
        screen.fill(BLACK)

        # Draw cells
        for i in range(WINDOW_SIZE):
            for j in range(WINDOW_SIZE):
                maze[i][j].draw()
        
        if len(stack) > 0:
            current = stack.pop()
            current.highlight()
			
            neighbours = has_unvisited_neighbors(maze, current)
            if len(neighbours) > 0:
                neighbour = choice(neighbours)

                stack.append(current)
                
                neighbour.visited = True
                
                remove_wall(current, neighbour)
                
                stack.append(neighbour)

        # Update window
        pygame.display.update()
        
        clock.tick(FPS)

    pygame.quit()
