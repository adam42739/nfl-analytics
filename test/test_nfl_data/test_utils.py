import pandas as pd
from nfl_analytics.nfl_data import utils
from nfl_analytics.nfl_data.utils import NflWeek


def test_nfl_week_advance():
    # Create an NflWeek object for the 2023 season, week 1
    week = NflWeek(2023, 1)

    # Advance the week by 1
    week.advance(1)

    # Check if the week is now 2
    assert week.week == 2

    # Check if the season is still 2023
    assert week.season == 2023

    # Advance the week by 20 (to the next season)
    week.advance(21)

    # Check if the week is now 1 and season is 2024
    assert week.week == 1
    assert week.season == 2024


def test_nfl_week_go_back():
    # Create an NflWeek object for the 2023 season, week 1
    week = NflWeek(2023, 1)

    # Go back the week by 1
    week.go_back(1)

    # Check if the week is now 22 (previous season)
    assert week.week == 22

    # Check if the season is now 2022
    assert week.season == 2022

    # Go back the week by 20 (to the previous season)
    week.go_back(20)

    # Check if the week is now 17 and season is still 2022
    assert week.week == 2
    assert week.season == 2022


def test_filter_data_weekly():
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
    filtered_df = utils.filter_data_weekly(
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
    filtered_df = utils.filter_data_weekly(df, end_week=end_week).reset_index(drop=True)

    # Check the result
    expected_data = {
        "season": [2022, 2023, 2023],
        "week": [1, 2, 3],
        "team": ["Team A", "Team B", "Team C"],
    }
    expected_df = pd.DataFrame(expected_data)

    assert filtered_df.equals(expected_df)

    # Filter the DataFrame: start_week onwards
    filtered_df = utils.filter_data_weekly(df, start_week=start_week).reset_index(
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


def test_filter_data_seasonaly():
    # Create a sample DataFrame
    data = {
        "season": [2022, 2023, 2023, 2024],
        "week": [1, 2, 3, 1],
        "team": ["Team A", "Team B", "Team C", "Team D"],
    }
    df = pd.DataFrame(data)

    # Define the start and end seasons
    start_season = 2023
    end_season = 2023

    # Filter the DataFrame: start_season to end_season
    filtered_df = utils.filter_data_seasonaly(
        df, start_season=start_season, end_season=end_season
    ).reset_index(drop=True)

    # Check the result
    expected_data = {
        "season": [2023, 2023],
        "week": [2, 3],
        "team": ["Team B", "Team C"],
    }
    expected_df = pd.DataFrame(expected_data)

    assert filtered_df.equals(expected_df)
