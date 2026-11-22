'''

La flota corresponde a un conjunto de barcos. Aquí se encuentran
operaciones para consultar su estado

'''

class Fleet:

    def __init__(self, ships):
        self.ships = ships

    @property
    def is_sunk(self):
        return all(ship.is_sunk for ship in self.ships)

    @property
    def remaining_ships(self):
        return [
            ship for ship in self.ships
            if not ship.is_sunk
        ]

    @property
    def remaining_lengths(self):
        return [
            ship.length for ship in self.remaining_ships
        ]

    def get_ship_at(self, cell):
        """Devuelve el barco que ocupa una casilla."""
        for ship in self.ships:
            if cell in ship.cells:
                return ship

        return None
