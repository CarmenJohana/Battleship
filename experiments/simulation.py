import random

from game.ship import Ship
from game.fleet import Fleet
from game.game_engine import GameEngine
from game.runner import GameRunner

from game.configurations import generate_configurations


def fleet_from_configuration(configuration, fleet_lengths):

    lengths = sorted(fleet_lengths, reverse=True)

    ships = []

    for ship_id, (length, placement) in enumerate(
        zip(lengths, configuration),
        start=1
    ):

        ships.append(
            Ship(
                ship_id=ship_id,
                length=length,
                cells=placement
            )
        )

    return Fleet(ships)



def run_single_game(
    n,
    configuration,
    fleet_lengths,
    agent_class,
    rng=None
):

    fleet = fleet_from_configuration(
        configuration,
        fleet_lengths
    )

    engine = GameEngine(n, fleet)

    agent = agent_class(n, rng=rng)

    runner = GameRunner(engine, agent)

    history = runner.run()

    return {
        "shots": engine.shots_fired,
        "history": history,
        "won": engine.has_won()
    }


def run_experiment(
    n,
    fleet_lengths,
    agent_classes,
    num_games,
    seed=None
):

    if num_games <= 0:
        raise ValueError("Number of games must be positive.")

    rng = random.Random(seed)

    configurations = generate_configurations(
        n,
        fleet_lengths
    )

    if not configurations:
        raise ValueError("No legal configurations available.")

    results = {
        agent_class.__name__: []
        for agent_class in agent_classes
    }

    for game_id in range(num_games):

        # One hidden fleet configuration per game.
        configuration = rng.choice(configurations)

        for agent_class in agent_classes:

            # Independent random generator for each agent.
            agent_seed = rng.getrandbits(64)
            agent_rng = random.Random(agent_seed)

            result = run_single_game(
                n=n,
                configuration=configuration,
                fleet_lengths=fleet_lengths,
                agent_class=agent_class,
                rng=agent_rng
            )

            result["game_id"] = game_id

            results[agent_class.__name__].append(result)

    return results

