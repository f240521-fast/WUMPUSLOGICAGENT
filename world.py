import random


class WumpusWorld:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.agent_pos = (0, 0)

        self.grid = [["" for _ in range(cols)] for _ in range(rows)]
        self.visited = set()
        self.visited.add((0, 0))

        self.place_hazards()

    def place_hazards(self):
        safe_start = (0, 0)

        # Place Wumpus
        while True:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (r, c) != safe_start:
                self.grid[r][c] = "W"
                break

        # Place pits
        pit_count = max(1, (self.rows * self.cols) // 5)

        for _ in range(pit_count):
            while True:
                r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
                if (r, c) != safe_start and self.grid[r][c] == "":
                    self.grid[r][c] = "P"
                    break

    def get_neighbors(self, pos):
        r, c = pos
        neighbors = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors.append((nr, nc))

        return neighbors

    def get_percepts(self, pos):
        percepts = []

        for nr, nc in self.get_neighbors(pos):
            if self.grid[nr][nc] == "P":
                percepts.append("Breeze")
            if self.grid[nr][nc] == "W":
                percepts.append("Stench")

        return percepts

    def move_agent(self, kb):
        neighbors = self.get_neighbors(self.agent_pos)

        for cell in neighbors:
            if cell not in self.visited:
                if kb.ask_safe(cell):
                    self.agent_pos = cell
                    self.visited.add(cell)
                    return "Moved Safely"

        return "No Safe Move"

    def get_visible_grid(self):
        visible = []

        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                if (r, c) == self.agent_pos:
                    row.append("A")
                elif (r, c) in self.visited:
                    row.append("S")
                else:
                    row.append("?")
            visible.append(row)

        return visible
