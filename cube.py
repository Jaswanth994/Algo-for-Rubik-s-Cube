# cube.py

class RubiksCube:
    """
    3x3x3 Rubik's Cube
    - Each cube has 6 faces: U (0), R (1), F (2), D (3), L (4), B (5)
    - Each face has 9 stickers, so state is a flat list of 54 integers.
    - Moves: U, D, F, B, L, R and their primes (')
    """

    FACE_INDICES = {
        'U': list(range(0, 9)),
        'R': list(range(9, 18)),
        'F': list(range(18, 27)),
        'D': list(range(27, 36)),
        'L': list(range(36, 45)),
        'B': list(range(45, 54))
    }

    # Mapping of edges per move:
    EDGE_MAPS = {
        'U': [
            [36, 37, 38],   # L top
            [18, 19, 20],   # F top
            [9, 10, 11],    # R top
            [45, 46, 47]    # B top
        ],
        'D': [
            [24, 25, 26],   # F bottom
            [42, 43, 44],   # L bottom
            [51, 52, 53],   # B bottom
            [15, 16, 17]    # R bottom
        ],
        'F': [
            [6, 7, 8],      # U bottom row
            [36, 39, 42],   # L right col (from top to bottom)
            [27, 28, 29],   # D top row (reversed)
            [11, 14, 17]    # R left col (from bottom to top)
        ],
        'B': [
            [2, 1, 0],      # U top row (reversed)
            [9, 12, 15],    # R right col (top to bottom)
            [33, 34, 35],   # D bottom row (reversed)
            [44, 41, 38]    # L left col (bottom to top)
        ],
        'L': [
            [0, 3, 6],      # U left col (top to bottom)
            [18, 21, 24],   # F left col (top to bottom)
            [27, 30, 33],   # D left col (top to bottom)
            [45, 48, 51]    # B right col (bottom to top)
        ],
        'R': [
            [8, 5, 2],      # U right col (top to bottom)
            [47, 50, 53],   # B left col (bottom to top)
            [35, 32, 29],   # D right col (top to bottom)
            [20, 23, 26]    # F right col (top to bottom)
        ]
    }

    def __init__(self, state=None):
        if state:
            self.state = state[:]
        else:
            self.state = [i // 9 for i in range(54)]

    def copy(self):
        return RubiksCube(self.state[:])

    def is_solved(self):
        return all(self.state[i*9:(i+1)*9].count(self.state[i*9]) == 9 for i in range(6))

    def apply_move(self, move):
        """
        Apply a move. move: one of 'U','U\'','D','D\'','F','F\'','B','B\'','L','L\'','R','R\''
        """
        if len(move) == 1:
            self._face_move(move, prime=False)
        elif move[1] == "'":
            self._face_move(move[0], prime=True)
        else:
            raise ValueError("Unsupported move notation.")

    def _face_move(self, face, prime=False):
        """
        Rotate a face (clockwise by default; counter-clockwise if prime).
        """
        # 1. Rotate the face's own stickers
        self._rotate_face(self.FACE_INDICES[face], ccw=prime)
        # 2. Cycle the edge stickers using mapping
        self._cycle_edges(self.EDGE_MAPS[face], ccw=prime)

    def _rotate_face(self, indices, ccw=False):
        """
        Rotate a face's 9 stickers (indices: list of 9 ints), 90° (clockwise or counter-clockwise)
        """
        s = self.state
        out = s[:]
        if not ccw:
            mapping = [6, 3, 0, 7, 4, 1, 8, 5, 2]  # Clockwise
        else:
            mapping = [2, 5, 8, 1, 4, 7, 0, 3, 6]  # Counter-clockwise
        for idx, map_to in zip(indices, mapping):
            out[idx] = s[indices[map_to]]
        self.state = out

    def _cycle_edges(self, edge_groups, ccw=False):
        """
        Rotate four edge groups (list of [a, b, c]) for a given move.
        Each group is a list of 3 indices.
        """
        s = self.state
        out = self.state[:]
        if not ccw:
            for i in range(4):
                src = edge_groups[(i-1)%4]
                dst = edge_groups[i]
                for j in range(3):
                    out[dst[j]] = s[src[j]]
        else:
            for i in range(4):
                src = edge_groups[(i+1)%4]
                dst = edge_groups[i]
                for j in range(3):
                    out[dst[j]] = s[src[j]]
        self.state = out

    def __str__(self):
        """Nice ASCII view for debugging."""
        color = ['W', 'R', 'G', 'Y', 'O', 'B']
        face = lambda idxs: '\n'.join(' '.join(color[self.state[i]] for i in idxs[j:j+3]) for j in range(0, 9, 3))
        return (
            "    " + ' '.join(color[self.state[i]] for i in range(0,3)) + "\n" +
            "    " + ' '.join(color[self.state[i]] for i in range(3,6)) + "\n" +
            "    " + ' '.join(color[self.state[i]] for i in range(6,9)) + "\n" +
            '\n'.join(
                ' '.join(color[self.state[i]] for i in row)
                for row in [
                    [36,37,38, 18,19,20, 9,10,11, 45,46,47],
                    [39,40,41, 21,22,23,12,13,14, 48,49,50],
                    [42,43,44, 24,25,26,15,16,17, 51,52,53],
                ]
            ) + "\n" +
            "    " + ' '.join(color[self.state[i]] for i in range(27,30)) + "\n" +
            "    " + ' '.join(color[self.state[i]] for i in range(30,33)) + "\n" +
            "    " + ' '.join(color[self.state[i]] for i in range(33,36)) + "\n"
        )
