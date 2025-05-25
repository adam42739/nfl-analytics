import tempfile
from nfl_analytics import _local_storage
from typing import Callable
import pandas as pd
from nfl_analytics.nfl_data import basic_data


def run_data_fetch_test(
    data_fetcher: Callable[[], pd.DataFrame],
    expected_columns: list[str],
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
            df = data_fetcher(**fetcher_args)

            # Check that the DataFrame has the expected columns
            for col in expected_columns:
                assert col in df.columns

            # Check that the file exists in the datastore
            assert _local_storage.file_exists("nfl_data/", file_path)
        finally:
            # Reset the datastore path to the original path
            _local_storage.set_datastore_path(current_path)


def test_schedules():
    # Define the expected columns
    expected_columns = [
        "game_id",
        "season",
        "week",
        "home_team",
        "away_team",
        "home_score",
        "away_score",
    ]

    # Define the file path
    file_path = f"schedules.parquet"

    # Run the data fetch test
    run_data_fetch_test(
        basic_data.schedules,
        expected_columns,
        file_path,
        start_week=basic_data.NflWeek(2023, 1),
        end_week=basic_data.NflWeek(2023, 18),
    )


def test_pbp():
    # Define the expected columns
    expected_columns = [
        "game_id",
        "play_id",
        "season",
        "week",
        "home_team",
        "away_team",
        "posteam",
        "defteam",
    ]

    # Define the file path
    file_path = f"pbp-year=2023.parquet"

    # Run the data fetch test
    run_data_fetch_test(
        basic_data.pbp,
        expected_columns,
        file_path,
        start_week=basic_data.NflWeek(2023, 1),
        end_week=basic_data.NflWeek(2023, 18),
    )