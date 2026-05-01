class KnowledgeBase:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.rules = []
        self.safe_cells = {(0, 0)}
        self.inference_steps = 0

    def tell(self, position, percepts):
        r, c = position

        if "Breeze" not in percepts and "Stench" not in percepts:
            neighbors = self.get_neighbors(position)

            for n in neighbors:
                self.safe_cells.add(n)

        self.rules.append((position, percepts))

    def ask_safe(self, cell):
        self.inference_steps += 1

        if cell in self.safe_cells:
            return True

        return False

    def get_neighbors(self, pos):
        r, c = pos
        neighbors = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors.append((nr, nc))

        return neighbors
