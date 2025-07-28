
---

````markdown
# Rubik's Cube Solver — AeroHack 2025 - CS

---

## Overview

This project implements a Rubik’s Cube solver designed for hackathon competitions, balancing **algorithmic rigor**, **practical efficiency**, and **user-friendly interaction**. The solution uses an `A*` search algorithm enhanced with move pruning, heuristic evaluation, and parallelization to find solutions quickly without excessive memory consumption.

The system features:

- A **core cube data model** to represent and manipulate the 3x3x3 cube.
- An **optimized `A*` solver** capable of solving typical scrambles within seconds.
- A **command-line interface** to demonstrate solving and verify correctness.
- A **graphical user interface (GUI)** for interactive cube manipulation, scrambling, and solution visualization.
- Comprehensive **unit tests** validating solver correctness, timing, and robustness across fixed and random scrambles.

---

## Project Structure

```text
.
├── cube.py          # Rubik's Cube logic, move definitions, state management
├── solver.py        # A* search solver with heuristics, pruning, and parallelization
├── main.py          # Command-line driver script demonstrating solve from scramble
├── gui.py           # Tkinter GUI with scramble, manual moves, animation, and solve
├── tests.py         # Unit tests for validating cube and solver functionality
└── README.md        # This documentation file
````

---

## Features

### Cube Model (`cube.py`)

* Represents the cube’s 54 stickers in a flat list.
* Implements standard face moves (U, D, F, B, L, R) and their inverses.
* Supports checking for solved state and printing ASCII representation.

### Solver (`solver.py`)

* Implements an `A*` search with:

  * An admissible heuristic counting misplaced stickers.
  * Move pruning to skip redundant or inverse moves.
  * Timeout and maximum depth to prevent infinite loops.
  * Optional parallelization exploring first moves concurrently.
* Designed for hackathon performance: solves typical scrambles in seconds.

### Command-line Interface (`main.py`)

* Applies a predefined scramble to the cube.
* Runs the solver with configurable depth and timeout.
* Prints the scramble, solution, move count, solving time, and post-solution cube state.

### Graphical User Interface (`gui.py`)

* Visualizes the cube as a 2D net with colored stickers.
* Supports manual moves via clickable buttons.
* Allows customizable scrambles with adjustable length.
* Provides real-time solve animation using the solver.
* Displays scramble and solution sequences with undo functionality.

### Testing (`tests.py`)

* Unit tests cover:

  * The solved cube edge case to ensure solver correctness without moves.
  * Fixed known scrambles for correctness and performance.
  * Random scramble batches with timeout guards for robustness.
* Ensures solution correctness by verifying the cube’s solved state post-solving.

---

## Requirements

* Python 3.7 or newer
* Standard library only (no external dependencies required)

---

## How to Run

### Command-line Solve Example

```bash
python main.py
```

This will scramble the cube with a preset sequence, attempt to solve using `A*` search, and display solution steps and timings.

### Launch GUI

```bash
python gui.py
```

The GUI provides an interactive experience with:

* Buttons for manual moves and scramble
* Slider to control scramble length
* Visual feedback and animated solution
* Undo, reset, and status messages

### Run Unit Tests

```bash
python tests.py
```

Automated tests provide confidence in solver correctness and efficiency.

---

## Algorithmic Notes

* **Heuristic:** Counts misplaced stickers normalized to keep admissibility, striking a balance between efficiency and accuracy.
* **Move Pruning:** Skips consecutive moves on the same face and immediate inverse moves to reduce state explosion.
* **Parallelization:** First-layer branching is parallelized using threading, speeding up solution search.
* **Timeouts:** Configurable time limits prevent stalls and infinite loops typical in combinatorial search.
* **Potential Extensions:** Future improvements include IDA\*, pattern databases, or Kociemba’s two-phase algorithm for more optimal and faster solving.

---

## Performance

* Typical solves of 8–12 move scrambles complete within 5–10 seconds on standard hardware.
* Maximum tested search depth is 22 moves, adequate for hackathon-level challenges.
* Parallel solving further reduces effective solving time on multicore machines.

---

## Future Work

* Implement IDA\* search for memory-efficient deep solving.
* Integrate pattern databases for improved heuristic accuracy.
* Enhance GUI with 3D cube visualization and drag/mouse interaction.
* Add scramble randomizer ensuring only valid cube states.

---

## Contact & Collaboration

Feel free to open issues, fork, or contribute pull requests.

Good luck reviewing, and thank you for considering this project.

---

*Prepared by,
Jaswanth Gosu (Hackathon Contestant)*

```
