
import cProfile
import pstats

from agents.maximum_probability_agent import MaximumProbabilityAgent
from agents.maximum_information_gain_agent import MaximumInformationGainAgent
from experiments.simulation import run_experiment


def profile_agent(agent_class, n, fleet_lengths, num_games=10):
    print(f"\nPROFILE: {agent_class.__name__}")
    print("=" * 70)

    profiler = cProfile.Profile()

    profiler.enable()

    run_experiment(
        n=n,
        fleet_lengths=fleet_lengths,
        agent_classes=[agent_class],
        num_games=num_games,
        seed=42,
    )

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats("cumulative")
    stats.print_stats(20)


if __name__ == "__main__":
    agents = [
        MaximumProbabilityAgent,
        MaximumInformationGainAgent,
    ]

    for agent_class in agents:
        profile_agent(
            agent_class,
            n=5,
            fleet_lengths=[4, 3, 2],
            num_games=10,
        )
