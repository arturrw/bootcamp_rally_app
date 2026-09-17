import random

import pandas as pd


def simulate_race(cars: pd.DataFrame) -> pd.DataFrame:
    """Run one race over the given cars and return results sorted by finish time (fastest first)."""
    results = []
    for _, row in cars.iterrows():
        base_time = 100 / row["MAX_SPEED"]
        penalty = random.uniform(0, (1 - row["RELIABILITY"]))
        total_time = base_time + penalty
        results.append((row["TEAM_ID"], row["TEAM_NAME"], row["CAR_NAME"], total_time))

    columns = ["team_id", "team_name", "car_name", "time"]
    return pd.DataFrame(results, columns=columns).sort_values("time").reset_index(drop=True)


def pick_winner(results: pd.DataFrame) -> pd.Series:
    """Return the winning row from race results already sorted by time."""
    return results.iloc[0]
