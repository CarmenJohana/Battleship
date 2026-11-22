
from itertools import combinations

from agents.random_agent import RandomAgent
from agents.maximum_probability_agent import MaximumProbabilityAgent
from agents.maximum_information_gain_agent import (
    MaximumInformationGainAgent
)

from experiments.simulation import run_experiment

from experiments.evaluation import (
    evaluate_results,
    print_evaluation,
    compare_agents_paired,
    print_paired_comparison
)


n = 5
fleet_lengths = [3, 2]
num_games = 1000
seed = 42

agent_classes = [
    RandomAgent,
    MaximumProbabilityAgent,
    MaximumInformationGainAgent
]

results = run_experiment(
    n=n,
    fleet_lengths=fleet_lengths,
    agent_classes=agent_classes,
    num_games=num_games,
    seed=seed
)

# Individual evaluation.
evaluation = evaluate_results(results)

print("\nEXPERIMENTAL RESULTS")
print_evaluation(evaluation)

# Paired comparisons.
print("\nPAIRED COMPARISONS")

agent_names = [
    agent_class.__name__
    for agent_class in agent_classes
]

for agent_a, agent_b in combinations(agent_names, 2):

    comparison = compare_agents_paired(
        results,
        agent_a,
        agent_b
    )

    print_paired_comparison(comparison)

