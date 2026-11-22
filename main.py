
import random

from agents.random_agent import RandomAgent

from experiments.simulation import run_experiment
from experiments.evaluation import (
    evaluate_results,
    print_evaluation
)


n = 5
fleet_lengths = [3, 2]

num_games = 1000
seed = 42

agent_classes = [
    RandomAgent
]

results = run_experiment(
    n=n,
    fleet_lengths=fleet_lengths,
    agent_classes=agent_classes,
    num_games=num_games,
    seed=seed
)

evaluation = evaluate_results(results)

print("\nEXPERIMENTAL RESULTS")
print_evaluation(evaluation)

