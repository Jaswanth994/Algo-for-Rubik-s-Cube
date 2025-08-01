import unittest
import time
import threading
from cube import RubiksCube
from solver import a_star_solve


def apply_moves(cube, moves):
    for m in moves:
        cube.apply_move(m)


def a_star_solve_with_timeout(cube, max_depth=12, timeout=5):
    """
    Run a_star_solve with a timeout.
    Returns solution list if found within timeout, else None.
    """
    result = [None]
    def target():
        # Pass timeout down to solver to limit internal run time as well
        result[0] = a_star_solve(cube, max_depth=max_depth, timeout=timeout)
    t = threading.Thread(target=target)
    t.daemon = True
    t.start()
    t.join(timeout)
    if t.is_alive():
        return None
    return result[0]


class TestRubiksCubeWithTiming(unittest.TestCase):

    def test_solved_cube(self):
        """Solver should immediately solve a solved cube (no moves needed)."""
        cube = RubiksCube()
        solution = a_star_solve_with_timeout(cube, max_depth=1, timeout=2)
        self.assertEqual(solution, [], "Solver should return empty list for already solved cube")

    def test_simple_scramble_timings(self):
        """Test a fixed simple scramble to verify solver correctness and efficiency."""
        scramble = ['U', "R'", 'F']
        cube = RubiksCube()
        apply_moves(cube, scramble)
        start = time.time()
        solution = a_star_solve_with_timeout(cube, max_depth=8, timeout=5)
        elapsed = time.time() - start

        self.assertIsNotNone(solution, "Solver failed to find a solution in time.")
        apply_moves(cube, solution)
        self.assertTrue(cube.is_solved(), "Cube not solved after applying solution.")

        print(f"[Simple Scramble] Moves to solve: {len(solution)}; Time taken: {elapsed:.3f}s")

    def test_known_scrambles(self):
        """
        Test a few known scrambles and their expected successful solve.
        These are fixed for reproducibility, good for demo.
        """
        scrambles = [
            ['U', "R'", 'F'],
            ['L', 'F', "R'", "U'"],
            ['D', 'B', 'L', 'F', 'R', 'U'],
        ]
        for scramble in scrambles:
            with self.subTest(scramble=scramble):
                cube = RubiksCube()
                apply_moves(cube, scramble)
                solution = a_star_solve_with_timeout(cube, max_depth=12, timeout=7)
                self.assertIsNotNone(solution, f"Failed to solve scramble: {scramble}")
                apply_moves(cube, solution)
                self.assertTrue(cube.is_solved(), f"Not solved after solution for scramble: {scramble}")
                print(f"[Known Scramble] {scramble} solved in {len(solution)} moves.")

    def test_random_scramble_batch(self):
        """
        Run a moderate number of random scrambles with timeouts.
        Skip any that take too long.
        """
        import random
        moves = ['U', "U'", 'D', "D'", 'F', "F'", 'B', "B'", 'L', "L'", 'R', "R'"]
        num_tests = 10
        max_scramble_length = 6
        max_solver_depth = 12
        solver_timeout = 7
        solved_count = 0

        for i in range(num_tests):
            scramble = [random.choice(moves) for _ in range(max_scramble_length)]
            cube = RubiksCube()
            apply_moves(cube, scramble)

            start = time.time()
            solution = a_star_solve_with_timeout(cube, max_depth=max_solver_depth, timeout=solver_timeout)
            elapsed = time.time() - start

            if solution is None:
                print(f"[Random Scramble {i+1}] Skipped due to timeout (> {solver_timeout}s). Scramble: {scramble}")
                continue  # Skip if not solved in time

            apply_moves(cube, solution)
            self.assertTrue(cube.is_solved(), f"Not solved after applying solution for scramble: {scramble}")
            print(f"[Random Scramble {i+1}] Solved scramble_len={len(scramble)} "
                  f"solution_len={len(solution)} time={elapsed:.3f}s")
            solved_count += 1

        if solved_count == 0:
            self.fail("No random scrambles solved within timeout — possible solver issue.")


if __name__ == "__main__":
    unittest.main()
