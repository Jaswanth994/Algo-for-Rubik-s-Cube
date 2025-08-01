# gui.py

import tkinter as tk
from tkinter import messagebox
from cube import RubiksCube
from solver import a_star_solve
import random
import threading

# Define colors for each cube face
COLOR_MAP = ['white', 'red', 'green', 'yellow', 'orange', 'blue']

MOVE_LIST = ['U', "U'", 'D', "D'", 'F', "F'", 'B', "B'", 'L', "L'", 'R', "R'"]

class CubeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rubik's Cube Solver GUI")
        self.resizable(False, False)
        self.cube = RubiksCube()
        self.scramble_sequence = []
        self.solution_sequence = []
        self._build_ui()
        self._draw_cube()

    def _build_ui(self):
        self.canvas = tk.Canvas(self, width=355, height=265, bg='gray90', highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=6, pady=10)

        # Control buttons
        row = 1
        for idx, move in enumerate(MOVE_LIST):
            b = tk.Button(self, text=move, width=3,
                          command=lambda m=move: self.do_move(m))
            b.grid(row=row, column=idx%6, padx=2, pady=2, sticky='nsew')
            if (idx+1)%6 == 0:
                row += 1

        # Extra controls with padding and styled
        tk.Button(self, text="Scramble", bg="#d0eaff", command=self.scramble).grid(row=row+1, column=0, padx=3, pady=8)
        self.scramble_len = tk.Scale(self, from_=4, to=14, orient='horizontal', label="Scramble Length", length=110)
        self.scramble_len.set(8)
        self.scramble_len.grid(row=row+1, column=1, columnspan=2, pady=8)

        tk.Button(self, text="Reset", bg="#f9dfcf", command=self.reset).grid(row=row+1, column=3, padx=3, pady=8)
        tk.Button(self, text="Solve", bg="#d4f5d8", fg='black', command=self.solve).grid(row=row+1, column=4, padx=3, pady=8)
        tk.Button(self, text="Undo", bg="#ffd6d6", command=self.undo_move).grid(row=row+1, column=5, padx=3, pady=8)

        self.status = tk.Label(self, text="", anchor='w', font=('Arial', 10), fg="#254441", bg='#e5f5f1')
        self.status.grid(row=row+2, column=0, columnspan=6, sticky='we', pady=4)
        self.protocol("WM_DELETE_WINDOW", self.destroy_gui)

        self.scramble_display = tk.Label(self, text="Scramble: ", anchor='w', font=('Consolas', 9), bg="#f6faf8")
        self.scramble_display.grid(row=row+3, column=0, columnspan=6, sticky='we')
        self.solution_display = tk.Label(self, text="Solution: ", anchor='w', font=('Consolas', 9), bg="#f6faf8")
        self.solution_display.grid(row=row+4, column=0, columnspan=6, sticky='we')

    def destroy_gui(self):
        self.destroy()

    def _draw_cube(self):
        # Coordinates for the 6 faces on a 2D net
        face_pos = {
            'U': (3, 0), 'L': (0, 3), 'F': (3, 3),
            'R': (6, 3), 'B': (9, 3), 'D': (3, 6)
        }
        size = 27
        self.canvas.delete("cubesticker")
        for idx, face in enumerate(['U','L','F','R','B','D']):
            fx, fy = face_pos[face]
            facelet = self.cube.state[idx*9:(idx+1)*9]
            for j in range(3):
                for i in range(3):
                    color = COLOR_MAP[facelet[j*3 + i]]
                    x0, y0 = (fx+i)*size+5, (fy+j)*size+5
                    x1, y1 = x0+size-2, y0+size-2
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black', tags="cubesticker")

    def do_move(self, move):
        self.cube.apply_move(move)
        self.solution_sequence.append(move)
        self._draw_cube()
        self.status.config(text=f'Applied move: {move}')
        self.update_solution_display()

    def undo_move(self):
        # Undo last manual move (if any)
        if self.solution_sequence:
            last_move = self.solution_sequence.pop()
            inv_move = last_move[0] + ("'" if "'" not in last_move else "")
            self.cube.apply_move(inv_move)
            self._draw_cube()
            self.status.config(text=f'Undid move: {last_move}')
            self.update_solution_display()

    def scramble(self):
        n = self.scramble_len.get()
        self.reset()
        scramble_moves = []
        last_face = None
        for _ in range(n):
            move = random.choice(MOVE_LIST)
            # Ensure no same-face as previous for better scrambles
            while last_face is not None and move[0] == last_face:
                move = random.choice(MOVE_LIST)
            scramble_moves.append(move)
            self.cube.apply_move(move)
            last_face = move[0]
        self.scramble_sequence = scramble_moves
        self.solution_sequence.clear()
        self._draw_cube()
        self.status.config(text=f'Scrambled ({n}): {" ".join(scramble_moves)}')
        self.update_scramble_display()
        self.update_solution_display()

    def reset(self):
        self.cube = RubiksCube()
        self.scramble_sequence.clear()
        self.solution_sequence.clear()
        self._draw_cube()
        self.status.config(text='Cube reset to solved state.')
        self.update_scramble_display()
        self.update_solution_display()

    def solve(self):
        self.status.config(text="Solving... Please wait.")
        self.update()
        scramble_snapshot = self.scramble_sequence.copy()

        def solver_thread():
            solution = a_star_solve(self.cube, max_depth=40, timeout=30)
            if solution:
                # Animate application
                for move in solution:
                    self.cube.apply_move(move)
                    self._draw_cube()
                    self.status.config(text=f"Solving... move: {move}")
                    self.update()
                    self.after(180)
                self.status.config(text=f"Solved! Moves: {' '.join(solution)} (len={len(solution)})")
                self.solution_sequence = solution
                self.update_solution_display()
            else:
                self.status.config(text="No solution found (try longer timeout/depth for harder scrambles).")
                self.solution_sequence = []
                self.update_solution_display()

        t = threading.Thread(target=solver_thread)
        t.daemon = True
        t.start()

    def update_scramble_display(self):
        scramble_txt = f"Scramble: {' '.join(self.scramble_sequence) if self.scramble_sequence else '(solved)'}"
        self.scramble_display.config(text=scramble_txt)

    def update_solution_display(self):
        solution_txt = f"Solution: {' '.join(self.solution_sequence) if self.solution_sequence else ''}"
        self.solution_display.config(text=solution_txt)

if __name__ == "__main__":
    CubeGUI().mainloop()
