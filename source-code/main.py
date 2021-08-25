import create
from maze import Maze
from solver import Solver

if __name__ == '__main__':
    # 10 = (10*2)+1 = 21

    # maze = Maze(create.Maze(12, 12, 0))
    # Solver(maze, algorithm='BFS').solve()

    for i in range(0, 3):
        # 25x25
        maze = Maze(create.Maze(12, 12, i))
        Solver(maze, algorithm='BFS').solve()
        Solver(maze, algorithm='ASTAR').solve()

        # 125x125
        maze = Maze(create.Maze(62, 62, i))
        Solver(maze, algorithm='BFS').solve()
        Solver(maze, algorithm='ASTAR').solve()

        # 525x525
        maze = Maze(create.Maze(262, 262, i))
        Solver(maze, algorithm='BFS').solve()
        Solver(maze, algorithm='ASTAR').solve()
