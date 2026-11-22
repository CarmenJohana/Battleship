import time

from game.configurations import generate_configurations
from agents.random_agent import RandomAgent
from agents.maximum_probability_agent import MaximumProbabilityAgent
from agents.maximum_information_gain_agent import MaximumInformationGainAgent
from experiments.simulation import run_experiment



def benchmark_simulation(n, fleet_lengths, num_games=100):
    agent_classes = [
        RandomAgent,
        MaximumProbabilityAgent,
        MaximumInformationGainAgent,
    ]

    print("\nINDIVIDUAL AGENT BENCHMARK")
    print("-" * 75)

    print(
        f"{'Agent':<35}"
        f"{'Total time (s)':>18}"
        f"{'Time/game (s)':>18}"
    )

    print("-" * 75)

    for agent_class in agent_classes:
        start = time.perf_counter()

        run_experiment(
            n=n,
            fleet_lengths=fleet_lengths,
            agent_classes=[agent_class],
            num_games=num_games,
            seed=42,
        )

        elapsed = time.perf_counter() - start

        print(
            f"{agent_class.__name__:<35}"
            f"{elapsed:>18.4f}"
            f"{elapsed / num_games:>18.4f}"
        )



def benchmark_generation(experiments):
    print("\nCONFIGURATION GENERATION BENCHMARK")
    print("-" * 75)

    print(
        f"{'Board':<10}"
        f"{'Fleet':<20}"
        f"{'Configurations':>20}"
        f"{'Time (s)':>15}"
    )

    print("-" * 75)

    for experiment in experiments:
        n = experiment["n"]
        fleet_lengths = experiment["fleet_lengths"]

        start = time.perf_counter()

        configurations = generate_configurations(
            n,
            fleet_lengths
        )

        elapsed = time.perf_counter() - start

        print(
            f"{n}x{n:<8}"
            f"{str(fleet_lengths):<20}"
            f"{len(configurations):>20,}"
            f"{elapsed:>15.6f}"
        )


if __name__ == "__main__":
    experiments = [
        {"n": 5, "fleet_lengths": [2, 2]},
        {"n": 5, "fleet_lengths": [3, 2]},
        {"n": 5, "fleet_lengths": [3, 3]},
        {"n": 5, "fleet_lengths": [4, 3, 2]},
    ]

    benchmark_generation(experiments)
    benchmark_simulation(
	    n=5,
	    fleet_lengths=[4, 3, 2],
	    num_games=100,
	)
