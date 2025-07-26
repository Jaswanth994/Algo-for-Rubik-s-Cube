# main.py

from cube import RubiksCube
from solver import a_star_solve

def print_solution(scramble, solution):
    print("Scramble applied:", ' '.join(scramble))
    if solution is None:
        print("No solution found within the search depth or time constraints.")
    else:
        print("Solution moves:", ' '.join(solution))
        print("Number of moves:", len(solution))

if __name__ == "__main__":
    # You can change or randomize the scramble as needed
    scramble_moves = ['U', "R'", 'F', 'L', "D'", 'B']
    cube = RubiksCube()
    for move in scramble_moves:
        cube.apply_move(move)
    print("Initial scrambled cube (ASCII visualization):\n")
    print(cube)

    print("\nSolving optimally with A* search + heuristics...\n")
    solution = a_star_solve(cube, max_depth=16)
    print_solution(scramble_moves, solution)

    # Apply solution and show final state
    if solution:
        for move in solution:
            cube.apply_move(move)
        print("\nCube state after applying solution (should be solved):")
        print(cube)
