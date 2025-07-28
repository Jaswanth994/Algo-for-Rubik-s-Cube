# gui.py

import tkinter as tk
from cube import RubiksCube
from solver import a_star_solve
import random

# Define colors for each cube face
COLOR_MAP = ['white', 'red', 'green', 'yellow', 'orange', 'blue']

MOVE_LIST = ['U', "U'", 'D', "D'", 'F', "F'", 'B', "B'", 'L', "L'", 'R', "R'"]

class CubeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rubik's Cube Solver GUI")
        self.cube = RubiksCube()
        self.canvas = tk.Canvas(self, width=330, height=260, bg='gray90')
        self.canvas.pack()
        self._draw_cube()
        
        # Control buttons
        button_frame = tk.Frame(self)
        button_frame.pack()
        for move in MOVE_LIST:
            b = tk.Button(button_frame, text=move, width=3,
                          command=lambda m=move: self.do_move(m))
            b.pack(side=tk.LEFT)
        
        scramble_btn = tk.Button(self, text="Scramble (Random 8)", command=self.scramble)
        scramble_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(self, text="Reset", command=self.reset)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        solve_btn = tk.Button(self, text="Solve", command=self.solve)
        solve_btn.pack(side=tk.LEFT, padx=5)
        
        self.status = tk.Label(self, text="", anchor='w', font=('Arial', 10))
        self.status.pack(fill='x')
        
        self.protocol("WM_DELETE_WINDOW", self.destroy_gui)
        
    def destroy_gui(self):
        self.destroy()
        
    def _draw_cube(self):
        # Coordinates for the 6 faces on a 2D net
        face_pos = {
            'U': (3, 0), 'L': (0, 3), 'F': (3, 3),
            'R': (6, 3), 'B': (9, 3), 'D': (3, 6)
        }
        size = 25
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
        self._draw_cube()
        self.status.config(text=f'Applied move: {move}')
    
    def scramble(self):
        scramble_moves = [random.choice(MOVE_LIST) for _ in range(8)]
        for move in scramble_moves:
            self.cube.apply_move(move)
        self._draw_cube()
        self.status.config(text=f'Scrambled with: {" ".join(scramble_moves)}')
    
    def reset(self):
        self.cube = RubiksCube()
        self._draw_cube()
        self.status.config(text='Cube reset to solved state.')

    def solve(self):
        self.status.config(text="Solving...")
        self.update()
        solution = a_star_solve(self.cube, max_depth=16)
        if solution:
            for move in solution:
                self.cube.apply_move(move)
                self._draw_cube()
                self.update()
                self.after(100)  # Animate moves (100ms per move)
            self.status.config(text=f"Solved! Moves: {' '.join(solution)} (len={len(solution)})")
        else:
            self.status.config(text="No solution found or exceeded depth.")

if __name__ == "__main__":
    CubeGUI().mainloop()
