import tempfile
from nfl_analytics import _local_storage
from typing import Callable
import pandas as pd
from nfl_analytics.nfl_data import basic_data


def run_data_fetch_test(
    data_fetcher: Callable[[], pd.DataFrame],
    expected_head: pd.DataFrame,
    file_path: str,
    **fetcher_args,
):
    """
    Helper function to test data fetching functions.

    Parameters
    ----------
    data_fetcher : Callable
        The function to fetch data (e.g., nfl_data.get_players).
    expected_columns : list
        The list of expected columns in the resulting DataFrame.
    file_path : str
        The expected file path in the datastore.
    fetcher_args : dict
        Additional arguments to pass to the data_fetcher function.
    """
    with tempfile.TemporaryDirectory() as tempdir:
        # Get the current datastore path
        current_path = _local_storage._get_datastore_path()

        try:
            # Set the datastore path to a temporary directory
            _local_storage.set_datastore_path(tempdir)

            # Fetch the data
            df = data_fetcher(**fetcher_args).iloc[:5, :5].reset_index(drop=True)

            # Check that the DataFrames are equal
            assert df.equals(expected_head)

            # Check that the file exists in the datastore
            assert _local_storage.file_exists("nfl_data/", file_path)
        finally:
            # Reset the datastore path to the original path
            _local_storage.set_datastore_path(current_path)


def test_schedules():
    # Define the expected head (.iloc[:5,:5] of the DataFrame)
    expected_head = pd.DataFrame(
        [
            {
                "game_id": "2023_01_DET_KC",
                "season": 2023,
                "game_type": "REG",
                "week": 1,
                "gameday": "2023-09-07",
            },
            {
                "game_id": "2023_01_CAR_ATL",
                "season": 2023,
                "game_type": "REG",
                "week": 1,
                "gameday": "2023-09-10",
            },
            {
                "game_id": "2023_01_HOU_BAL",
                "season": 2023,
                "game_type": "REG",
                "week": 1,
                "gameday": "2023-09-10",
            },
            {
                "game_id": "2023_01_CIN_CLE",
                "season": 2023,
                "game_type": "REG",
                "week": 1,
                "gameday": "2023-09-10",
            },
            {
                "game_id": "2023_01_JAX_IND",
                "season": 2023,
                "game_type": "REG",
                "week": 1,
                "gameday": "2023-09-10",
            },
        ]
    )

    # Define the file path
    file_path = f"schedules.parquet"

    # Run the data fetch test
    run_data_fetch_test(
        basic_data.schedules,
        expected_head,
        file_path,
        start_week=basic_data.NflWeek(2023, 1),
        end_week=basic_data.NflWeek(2023, 18),
    )


def test_pbp():
    # Define the expected head (.iloc[:5,:5] of the DataFrame)
    expected_head = pd.DataFrame(
        [
            {
                "play_id": 1.0,
                "game_id": "2023_01_ARI_WAS",
                "old_game_id": "2023091007",
                "home_team": "WAS",
                "away_team": "ARI",
            },
            {
                "play_id": 39.0,
                "game_id": "2023_01_ARI_WAS",
                "old_game_id": "2023091007",
                "home_team": "WAS",
                "away_team": "ARI",
            },
            {
                "play_id": 55.0,
                "game_id": "2023_01_ARI_WAS",
                "old_game_id": "2023091007",
                "home_team": "WAS",
                "away_team": "ARI",
            },
            {
                "play_id": 77.0,
                "game_id": "2023_01_ARI_WAS",
                "old_game_id": "2023091007",
                "home_team": "WAS",
                "away_team": "ARI",
            },
            {
                "play_id": 102.0,
                "game_id": "2023_01_ARI_WAS",
                "old_game_id": "2023091007",
                "home_team": "WAS",
                "away_team": "ARI",
            },
        ]
    )

    # Define the file path
    file_path = f"pbp-year=2023.parquet"

    # Run the data fetch test
    run_data_fetch_test(
        basic_data.pbp,
        expected_head,
        file_path,
        start_week=basic_data.NflWeek(2023, 1),
        end_week=basic_data.NflWeek(2023, 18),
    )
