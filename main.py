# main.py

from cube import RubiksCube
from solver import bfs_solve

if __name__ == "__main__":
    # Example: scrambled state (custom or generated)
    original_cube = RubiksCube()
    scrambled = original_cube.copy()
    # Apply some moves to scramble (e.g., 'U', 'R', 'F')
    for mv in ['U', 'R', 'F']:
        scrambled.apply_move(mv)
    print("Solving scramble: U, R, F")
    solution = bfs_solve(scrambled)
    print("Solution:", solution)
