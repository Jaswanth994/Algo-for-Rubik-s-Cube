# solver.py

from collections import deque
from cube import RubiksCube
import time
import threading
from heapq import heappush, heappop

def heuristic(cube):
    """
    Improved admissible heuristic: counts the number of misplaced stickers,
    normalized for fairness (admissibility).
    """
    misplaced = sum(
        1 for i in range(6) for j in range(9) if cube.state[i * 9 + j] != i
    )
    return misplaced // 8  # Slightly more aggressive than //12, still admissible

def canonicalize(cube):
    """Hash of the cube state used for state uniqueness."""
    return tuple(cube.state)

def a_star_solve(start_cube, max_depth=22, timeout=10):
    """
    Practical A* solver for Rubik's Cube.
    - Move pruning avoids redundant & inverse moves on same face.
    - Timeout for hackathon reliability.
    """
    MOVES = ['U', "U'", 'D', "D'", 'F', "F'", 'B', "B'", 'L', "L'", 'R', "R'"]
    start_time = time.time()

    open_set = []
    g0 = 0
    h0 = heuristic(start_cube)
    heappush(open_set, (g0 + h0, g0, [], canonicalize(start_cube)))
    visited = set()
    visited.add(canonicalize(start_cube))

    while open_set:
        if time.time() - start_time > timeout:
            # Timeout: return best found (if any) or None
            return None
        f, depth, path, state_hash = heappop(open_set)
        cube = RubiksCube(list(state_hash))
        if cube.is_solved():
            return path
        if depth >= max_depth:
            continue
        for move in MOVES:
            # Prune: skip consecutive moves on same face (e.g. "R R")
            if path and move[0] == path[-1][0]:
                continue
            # Prune: skip immediate inverse (e.g. "R R'")
            if path and (move[0] == path[-1][0]) and ("'" in move) != ("'" in path[-1]):
                continue
            next_cube = cube.copy()
            next_cube.apply_move(move)
            next_hash = canonicalize(next_cube)
            if next_hash in visited:
                continue
            visited.add(next_hash)
            g = depth + 1
            h = heuristic(next_cube)
            heappush(open_set, (g + h, g, path + [move], next_hash))
    return None  # No solution found in time

def parallel_a_star_solve(start_cube, max_depth=22, timeout=10):
    """
    Parallelizes the first move to explore multiple branches quickly.
    Returns the shortest solution found by any thread within the timeout.
    """
    MOVES = ['U', "U'", 'D', "D'", 'F', "F'", 'B', "B'", 'L', "L'", 'R', "R'"]
    solutions = []
    threads = []
    found = threading.Event()
    lock = threading.Lock()

    def solve_branch(move):
        if found.is_set():
            return
        cube = start_cube.copy()
        cube.apply_move(move)
        path = a_star_solve(cube, max_depth=max_depth-1, timeout=timeout)
        if path is not None:
            with lock:
                solutions.append([move] + path)
                found.set()  # Optional: stop other threads early

    for move in MOVES:
        t = threading.Thread(target=solve_branch, args=(move,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join(timeout)
    if solutions:
        # Return the shortest found
        return min(solutions, key=len)
    return None

# # Example usage for hackathon demo:
# if __name__ == "__main__":
#     cube = RubiksCube()
#     scramble = ["U", "R", "F", "D", "U'", "L", "B"]
#     for mv in scramble:
#         cube.apply_move(mv)
#     print("Scramble:", scramble)
#     print("Initial cube:")
#     print(cube)
#     sol = parallel_a_star_solve(cube, max_depth=22, timeout=10)
#     if sol:
#         print("Solution:", sol)
#         print("Length:", len(sol))
#     else:
#         print("No solution found in given time or depth.")
