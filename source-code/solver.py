import time
from queue import PriorityQueue
from pathlib import Path

YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def save(algorithm, total_time, nodes, max_mem, size, difficulty):
    dados = {
        'algorithm': algorithm,
        'size': size,
        'difficulty': difficulty,
        'time': total_time,
        'nodes': nodes,
        'memory': max_mem
    }
    file = open(f'results/results.txt', 'a')
    file.write(str(dados) + "\n")
    file.close()


class Solver:
    def __init__(self, problem, algorithm='BFS', time_limit=float('inf'), start_time=0):
        self.num_visited = 0
        self.algorithm = algorithm
        self.problem = problem
        self.time_limit = time_limit
        self.start_time = start_time
        self.start = 0
        self.max_mem = -1
        self.size = self.problem.size
        self.difficulty = self.problem.difficulty
        Path(
            f'results/{self.size}/{self.difficulty}').mkdir(parents=True, exist_ok=True)

    def solve(self):
        self.start = time.time()
        print(f'Algorithm: {self.algorithm}')
        print(f'Difficulty: {self.difficulty}')
        print(f'Size: {self.size}')
        print(f'Start: {time.strftime("%H:%M:%S %d/%m/%Y", time.localtime())}')
        if self.algorithm == 'BFS':
            self.save_img(self.BFS(), RED, YELLOW)
        elif self.algorithm == 'ASTAR':
            self.save_img(self.ASTAR(), GREEN, YELLOW)
        end = time.time()
        print(f'\rNodes visited: {self.num_visited}')
        print(f'Nodes in memory: {self.max_mem}')
        print(f'Total time: {end - self.start} seconds\n')

        save(self.algorithm, end - self.start, self.num_visited,
             self.max_mem, self.size, self.difficulty)

    def save_img(self, results, color_res, color_vis):
        prev = results[0]
        path = []
        current = self.problem.end
        while current is not None:
            path.append(current)
            current = prev[current[0] * self.problem.size + current[1]]

        im = self.problem.im.convert('RGB')
        impixels = im.load()

        for n in results[1]:
            impixels[n[1], n[0]] = color_vis
        for n in path:
            impixels[n[1], n[0]] = color_res

        im.save(f'results/{self.size}/{self.difficulty}/{self.algorithm}.png')

    def print_nodes(self):
        print(f'\rNodes visited: {self.num_visited}', end='')

    def BFS(self):
        queue = [self.problem.start]
        path = []

        size = self.problem.size
        prev = [None] * (size * size)
        visited = [False] * (size * size)

        visited[self.problem.start[0] * size + self.problem.start[1]] = True

        while queue:
            if (time.time() - self.start) > self.time_limit:
                return 'TimeOut'
            self.num_visited += 1
            self.print_nodes()
            if self.max_mem < len(queue):
                self.max_mem = len(queue)

            node = queue.pop(0)

            if self.problem.is_target(node):
                return prev, path
            for suc, _ in self.problem.successors(node):
                npos = suc[0] * size + suc[1]
                if not visited[npos]:
                    queue.append(suc)
                    path.append(suc)
                    visited[npos] = True
                    prev[npos] = node

            # print(path)
            # print(queue)

    def heuristic(self, current):
        return abs((current[0] - self.problem.end[0])) + abs((current[1] - self.problem.end[1]))

    def ASTAR(self):
        queue = PriorityQueue()
        queue.put((0, self.problem.start))
        path = []

        prev = [None] * (self.problem.size * self.problem.size)
        visited = [False] * (self.problem.size * self.problem.size)
        visited[self.problem.start[0] *
                self.problem.size + self.problem.start[1]] = True

        while queue:
            if (time.time() - self.start) > self.time_limit:
                return 'TimeOut'
            self.num_visited += 1
            self.print_nodes()
            if self.max_mem < queue.qsize():
                self.max_mem = queue.qsize()

            cost, node = queue.get()
            path.append(node)
            if self.problem.is_target(node):
                break

            for suc, _ in self.problem.successors(node):
                npos = suc[0] * self.problem.size + suc[1]
                if not visited[npos]:
                    queue.put((1 + self.heuristic(suc), suc))
                    visited[npos] = True
                    prev[npos] = node

        return prev, path
