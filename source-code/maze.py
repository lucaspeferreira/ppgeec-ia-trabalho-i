from PIL import Image


class Maze:
    def __init__(self, maze):
        self.im = Image.open(maze.name)

        self.size = self.im.size[0]
        data = list(self.im.getdata(0))
        self.maze = []
        self.start = None
        self.end = None
        self.difficulty = maze.difficulty

        for i in range(self.size):
            self.maze.append(data[i * self.size:i * self.size + self.size])

        for x in range(self.size - 1):
            if self.maze[0][x] > 0:
                self.start = [0, x]
                break

        for x in range(self.size - 1):
            if self.maze[self.size - 1][x] > 0:
                self.end = [self.size - 1, x]
                break

    def successors(self, pos: list):
        x, y = pos
        successors = []

        if 0 < x < self.size - 1 and 0 < y < self.size - 1:
            if self.maze[x - 1][y] > 0:
                if x-1 > 0 and y-1 > 0:
                    successors.append([[x - 1, y], "U"])
            if self.maze[x][y - 1] > 0:
                successors.append([[x, y - 1], "L"])
            if self.maze[x][y + 1] > 0:
                successors.append([[x, y + 1], "R"])
            if self.maze[x + 1][y] > 0:
                successors.append([[x + 1, y], "D"])
        elif x <= 0:
            if self.maze[x + 1][y] > 0:
                successors.append([[x + 1, y], "D"])
        elif x >= self.size - 1:
            if self.maze[x - 1][y] > 0:
                successors.append([[x - 1, y], "U"])
        elif y <= 0:
            if self.maze[x][y + 1] > 0:
                successors.append([[x, y + 1], "R"])
        elif y >= self.size - 1:
            if self.maze[x][y - 1] > 0:
                successors.append([[x, y - 1], "L"])
        return successors

    def is_target(self, current: list):
        return current == self.end
