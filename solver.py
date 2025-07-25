# solver.py

from collections import deque
from cube import RubiksCube

def bfs_solve(start_cube):
    """
    Breadth-First Search solver: finds the shortest sequence of moves from start to solved.
    """
    moves = ['U', 'U\'', 'D', 'D\'', 'L', 'L\'', 'R', 'R\'', 'F', 'F\'', 'B', 'B\'']
    visited = set()
    queue = deque([(start_cube, [])])

    while queue:
        cube, path = queue.popleft()
        if cube.is_solved():
            return path
        state_tuple = tuple(cube.state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for move in moves:
            next_cube = cube.copy()
            next_cube.apply_move(move)
            queue.append((next_cube, path + [move]))
    return None  # Not found
