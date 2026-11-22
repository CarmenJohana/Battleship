
import statistics


def evaluate_results(results):

    evaluation = {}

    for agent_name, games in results.items():

        # Metadata is not an agent.
        if agent_name == "_metadata":
            continue

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

def compare_agents_paired(results, agent_a, agent_b):
    """
    Compare two agents using paired game results.

    Positive differences mean agent_a used fewer shots.
    Negative differences mean agent_b used fewer shots.

    Difference is defined as:
        shots_b - shots_a
    """

    if agent_a not in results or agent_b not in results:
        raise ValueError("One or both agents were not found.")

    games_a = results[agent_a]
    games_b = results[agent_b]

    # Index games by their game_id.
    indexed_a = {
        game["game_id"]: game
        for game in games_a
    }

    indexed_b = {
        game["game_id"]: game
        for game in games_b
    }

    if len(indexed_a) != len(games_a):
        raise ValueError(
            f"Duplicate game IDs found for {agent_a}."
        )

    if len(indexed_b) != len(games_b):
        raise ValueError(
            f"Duplicate game IDs found for {agent_b}."
        )

    if indexed_a.keys() != indexed_b.keys():
        raise ValueError(
            "Agents do not have matching game IDs."
        )

    differences = []

    wins_a = 0
    wins_b = 0
    ties = 0

    for game_id in sorted(indexed_a):

        game_a = indexed_a[game_id]
        game_b = indexed_b[game_id]

        # Both agents must face the same hidden fleet.
        if game_a["configuration"] != game_b["configuration"]:
            raise ValueError(
                f"Different fleet configurations in game {game_id}."
            )

        shots_a = game_a["shots"]
        shots_b = game_b["shots"]

        differences.append(shots_b - shots_a)

        if shots_a < shots_b:
            wins_a += 1
        elif shots_b < shots_a:
            wins_b += 1
        else:
            ties += 1

    num_games = len(differences)

    if num_games == 0:
        raise ValueError("No paired games available.")

    mean_difference = statistics.mean(differences)

    std_dev = (
        statistics.stdev(differences)
        if num_games > 1
        else 0.0
    )

    standard_error = (
        std_dev / (num_games ** 0.5)
        if num_games > 1
        else 0.0
    )

    # Approximate 95% confidence interval.
    margin_of_error = 1.96 * standard_error

    return {
        "agent_a": agent_a,
        "agent_b": agent_b,
        "num_games": num_games,
        "mean_difference": mean_difference,
        "median_difference": statistics.median(differences),
        "std_dev": std_dev,
        "standard_error": standard_error,
        "ci_95": (
            mean_difference - margin_of_error,
            mean_difference + margin_of_error
        ),
        "wins_a": wins_a,
        "wins_b": wins_b,
        "ties": ties,
        "win_rate_a": wins_a / num_games,
        "win_rate_b": wins_b / num_games,
        "tie_rate": ties / num_games
    }


def print_paired_comparison(comparison):

    agent_a = comparison["agent_a"]
    agent_b = comparison["agent_b"]

    ci_low, ci_high = comparison["ci_95"]

    print(f"\n{agent_a} vs {agent_b}")
    print("-" * 65)

    print(
        f"Paired games:       "
        f"{comparison['num_games']}"
    )

    print(
        f"Mean difference:    "
        f"{comparison['mean_difference']:.3f} shots"
    )

    print(
        f"Median difference:  "
        f"{comparison['median_difference']:.3f} shots"
    )

    print(
        f"Std deviation:      "
        f"{comparison['std_dev']:.3f}"
    )

    print(
        f"Standard error:     "
        f"{comparison['standard_error']:.3f}"
    )

    print(
        f"95% confidence interval: "
        f"[{ci_low:.3f}, {ci_high:.3f}]"
    )

    print(
        f"{agent_a} wins: "
        f"{comparison['wins_a']} "
        f"({comparison['win_rate_a']:.1%})"
    )

    print(
        f"{agent_b} wins: "
        f"{comparison['wins_b']} "
        f"({comparison['win_rate_b']:.1%})"
    )

    print(
        f"Ties:               "
        f"{comparison['ties']} "
        f"({comparison['tie_rate']:.1%})"
    )

