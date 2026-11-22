import random

from .ship import Ship
from .fleet import Fleet
from .configurations import generate_configurations


def generate_random_fleet(
    n: int,
    fleet_lengths: list[int],
    rng: random.Random | None = None
) -> Fleet:

    if not fleet_lengths:
        raise ValueError("Fleet must contain at least one ship.")

    # Generate every legal fleet configuration.
    configurations = generate_configurations(
        n,
        fleet_lengths
    )

    if not configurations:
        raise ValueError(
            "No legal fleet configurations available."
        )

    # Select one configuration uniformly at random.
    if rng is None:
        configuration = random.choice(configurations)
    else:
        configuration = rng.choice(configurations)

    # Ship lengths are sorted in the same way as in
    # generate_configurations().
    lengths = sorted(fleet_lengths, reverse=True)

    # Convert placements into Ship objects.
    ships = []

    for ship_id, (length, placement) in enumerate(
        zip(lengths, configuration),
        start=1
    ):

        ship = Ship(
            ship_id=ship_id,
            length=length,
            cells=placement
        )

        ships.append(ship)

    return Fleet(ships)
