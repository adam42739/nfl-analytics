import pandas as pd
from nfl_analytics.nfl_data import utils
from nfl_analytics.nfl_data.utils import NflWeek


def test_filter_data():
    # Create a sample DataFrame
    data = {
        "season": [2022, 2023, 2023, 2024],
        "week": [1, 2, 3, 1],
        "team": ["Team A", "Team B", "Team C", "Team D"],
    }
    df = pd.DataFrame(data)

    # Define the start and end weeks
    start_week = NflWeek(2023, 2)
    end_week = NflWeek(2023, 3)

    # Filter the DataFrame: start_week to end_week
    filtered_df = utils.filter_data(
        df, start_week=start_week, end_week=end_week
    ).reset_index(drop=True)

    # Check the result
    expected_data = {
        "season": [2023, 2023],
        "week": [2, 3],
        "team": ["Team B", "Team C"],
    }
    expected_df = pd.DataFrame(expected_data)

    assert filtered_df.equals(expected_df)

    # Filter the DataFrame: up to end_week
    filtered_df = utils.filter_data(df, end_week=end_week).reset_index(drop=True)

    # Check the result
    expected_data = {
        "season": [2022, 2023, 2023],
        "week": [1, 2, 3],
        "team": ["Team A", "Team B", "Team C"],
    }
    expected_df = pd.DataFrame(expected_data)

    assert filtered_df.equals(expected_df)

    # Filter the DataFrame: start_week onwards
    filtered_df = utils.filter_data(df, start_week=start_week).reset_index(
        drop=True
    )

    # Check the result
    expected_data = {
        "season": [2023, 2023, 2024],
        "week": [2, 3, 1],
        "team": ["Team B", "Team C", "Team D"],
    }
    expected_df = pd.DataFrame(expected_data)

    assert filtered_df.equals(expected_df)

