
import random
import hashlib

from game.ship import Ship
from game.fleet import Fleet
from game.game_engine import GameEngine
from game.runner import GameRunner

from game.configurations import generate_configurations


def derive_seed(master_seed, stream_id):
    """
    Derive a deterministic independent seed from a master seed
    and a unique stream identifier.
    """
    payload = f"{master_seed}:{stream_id}".encode("utf-8")

    digest = hashlib.blake2b(
        payload,
        digest_size=8,
        person=b"BattleshipRNG"
    ).digest()

    return int.from_bytes(digest, byteorder="big")


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

    agent = agent_class(
        n,
        fleet_lengths=fleet_lengths,
        rng=rng
    )

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

    # Generate an independent master seed if none was supplied.
    master_seed = (
        seed if seed is not None
        else random.SystemRandom().getrandbits(128)
    )

    # Dedicated random generator for fleet selection.
    fleet_seed = derive_seed(master_seed, "fleet")
    fleet_rng = random.Random(fleet_seed)

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

        # Select exactly one hidden fleet per game.
        configuration = fleet_rng.choice(configurations)

        for agent_class in agent_classes:

            # Identify the agent independently of its list position.
            agent_id = (
                f"{agent_class.__module__}."
                f"{agent_class.__qualname__}"
            )

            # Derive an independent seed for this agent and game.
            agent_seed = derive_seed(
                master_seed,
                f"agent:{agent_id}:game:{game_id}"
            )

            agent_rng = random.Random(agent_seed)

            result = run_single_game(
                n=n,
                configuration=configuration,
                fleet_lengths=fleet_lengths,
                agent_class=agent_class,
                rng=agent_rng
            )

            result["game_id"] = game_id

            # Store the hidden configuration as experimental metadata.
            # It is NOT passed to the agent.
            result["configuration"] = configuration

            results[agent_class.__name__].append(result)
            
    results["_metadata"] = {
        "seed": master_seed,
        "n": n,
        "fleet_lengths": list(fleet_lengths),
        "num_games": num_games
    }

    return results

