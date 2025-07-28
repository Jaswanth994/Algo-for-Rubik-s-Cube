# main.py

import time
from cube import RubiksCube
from solver import a_star_solve

def print_solution(scramble, solution, elapsed):
    print("Scramble applied:", ' '.join(scramble))
    if solution is None:
        print("No solution found within the search depth or time constraints.")
    else:
        print("Solution moves:", ' '.join(solution))
        print("Number of moves:", len(solution))
        print(f"Solving time: {elapsed:.3f} seconds")

if __name__ == "__main__":
    scramble_moves = ['U', "R'", 'F', 'L', "D'", 'B']  # Or generate/randomize
    cube = RubiksCube()
    for move in scramble_moves:
        cube.apply_move(move)

    print("Initial scrambled cube (ASCII visualization):\n")
    print(cube)

    print("\nSolving optimally with A* search + heuristics...\n")
    start_time = time.time()

    # Updated: Use recommended max_depth and timeout
    solution = a_star_solve(cube, max_depth=22, timeout=10)
    elapsed = time.time() - start_time

    print_solution(scramble_moves, solution, elapsed)

    if solution:
        for move in solution:
            cube.apply_move(move)
        print("\nCube state after applying solution (should be solved):")
        print(cube)
