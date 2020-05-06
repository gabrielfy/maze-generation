from random import choice
from math import ceil
import pygame


class Cell(object):
    border_size = 2

    def __init__(self, screen, size, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.screen = screen
        self.size = size
        self.borders = [True, True, True, True]  # top, right, bottom, left

    def draw(self):
        if self.visited:
            row, col = self.row * self.size, self.col * self.size
            # top
            if self.borders[0]:
                self._border((row, col), (row + self.size, col))
            # right
            if self.borders[1]:
                self._border((row + self.size, col),
                             (row + self.size, col + self.size))
            # bottom
            if self.borders[2]:
                self._border((row, col + self.size),
                             (row + self.size, col + self.size))
            # left
            if self.borders[3]:
                self._border((row, col), (row, col + self.size))

    def highlight(self):
        self._fill((0, 255, 0))

    def remove_wall(self, b):
        i = self.row - b.row
        if i == 1:
            self.borders[3] = False
            b.borders[1] = False
        elif i == -1:
            self.borders[1] = False
            b.borders[3] = False

        j = self.col - b.col
        if j == 1:
            self.borders[0] = False
            b.borders[2] = False
        elif j == -1:
            self.borders[2] = False
            b.borders[0] = False

    def _border(self, start_pos, end_pos):
        pygame.draw.line(self.screen, (255, 255, 255), start_pos,
                         end_pos, Cell.border_size)

    def _fill(self, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(
            self.row * self.size, self.col * self.size, self.size, self.size))


def has_unvisited_neighbors(maze, cell):
    neighbors = []
    number_of_cells = len(maze)

    # top
    if cell.row - 1 >= 0 and not maze[cell.row - 1][cell.col].visited:
        neighbors.append(maze[cell.row - 1][cell.col])
    # right
    if cell.col - 1 >= 0 and not maze[cell.row][cell.col - 1].visited:
        neighbors.append(maze[cell.row][cell.col - 1])
    # bottom
    if cell.row + 1 < number_of_cells and not maze[cell.row + 1][cell.col].visited:
        neighbors.append(maze[cell.row + 1][cell.col])
    # left
    if cell.col + 1 < number_of_cells and not maze[cell.row][cell.col + 1].visited:
        neighbors.append(maze[cell.row][cell.col + 1])

    return neighbors


def make_matrix(screen, cell_size):
    # Create matrix of cells
    screen_w = screen.get_width()

    number_of_cells = ceil(screen_w / cell_size)
    maze = []
    for i in range(number_of_cells):
        maze.append([])
        for j in range(number_of_cells):
            maze[i].append(
                Cell(screen, cell_size - ((cell_size + Cell.border_size) / screen_w), i, j))

    return maze


if __name__ == '__main__':

    # Define window
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Maze')

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

    # Stack of cells
    stack = []

    maze = make_matrix(screen, 20)

    # Start cell
    current = maze[0][0]
    current.visited = True
    stack.append(current)

    running = True
    while running:

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close window
                running = False

        # Set background color to black
        screen.fill((0, 0, 0))

        # Draw cells
        for row in maze:
            for cell in row:
                cell.draw()

        if len(stack) > 0:
            current = stack.pop()
            current.highlight()

            neighbours = has_unvisited_neighbors(maze, current)
            if len(neighbours) > 0:
                neighbour = choice(neighbours)
                neighbour.visited = True
                current.remove_wall(neighbour)
                stack.append(current)
                stack.append(neighbour)

        # Update window
        pygame.display.update()

        clock.tick(30)

    pygame.quit()
