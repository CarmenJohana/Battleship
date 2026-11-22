# Esto corresponde a la representación de un barco


from dataclasses import dataclass, field


@dataclass
class Ship:
    ship_id: int
    length: int
    cells: tuple[tuple[int, int], ...]

    hits: set[tuple[int, int]] = field(default_factory=set)

    def receive_hit(self, cell):
        """Registra un impacto sobre el barco."""
        if cell in self.cells:
            self.hits.add(cell)
            return True

        return False

    @property
    def is_sunk(self):
        """Indica si todas las casillas del barco fueron alcanzadas."""
        return len(self.hits) == self.length

    @property
    def remaining_cells(self):
        return set(self.cells) - self.hits

