import statistics


def evaluate_results(results):

    evaluation = {}

    for agent_name, games in results.items():

        if not games:
            raise ValueError(
                f"No games available for agent {agent_name}."
            )

        shots = [
            game["shots"]
            for game in games
        ]

        evaluation[agent_name] = {
            "num_games": len(shots),
            "mean": statistics.mean(shots),
            "median": statistics.median(shots),
            "variance": (
                statistics.variance(shots)
                if len(shots) > 1
                else 0.0
            ),
            "std_dev": (
                statistics.stdev(shots)
                if len(shots) > 1
                else 0.0
            ),
            "min": min(shots),
            "max": max(shots)
        }

    return evaluation


def print_evaluation(evaluation):

    headers = [
        "Agent",
        "Games",
        "Mean",
        "Median",
        "Std Dev",
        "Min",
        "Max"
    ]

    print(
        f"{headers[0]:<25}"
        f"{headers[1]:>8}"
        f"{headers[2]:>10}"
        f"{headers[3]:>10}"
        f"{headers[4]:>10}"
        f"{headers[5]:>8}"
        f"{headers[6]:>8}"
    )

    print("-" * 79)

    for agent_name, stats in evaluation.items():

        print(
            f"{agent_name:<25}"
            f"{stats['num_games']:>8}"
            f"{stats['mean']:>10.2f}"
            f"{stats['median']:>10.2f}"
            f"{stats['std_dev']:>10.2f}"
            f"{stats['min']:>8}"
            f"{stats['max']:>8}"
        )
