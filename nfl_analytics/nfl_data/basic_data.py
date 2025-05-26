import pandas as pd
from nfl_analytics.nfl_data import utils, _source_data
from nfl_analytics.nfl_data.utils import NflWeek


def schedules(
    start_week: NflWeek, end_week: NflWeek, force_refresh: bool = False
) -> pd.DataFrame:
    """
    Get the NFL schedules for the given weeks.

    Parameters
    ----------
        start_week : NflWeek
            The start week to get data from (inclusive).
        end_week : NflWeek
            The end week to get data to (inclusive).
        force_refresh : bool
            If True, we automatically get the most up-to-date data from NFL Verse and overwrite the local file.
    """
    df = _source_data.get("schedules", force_refresh)
    df = utils.filter_data_weekly(df, start_week, end_week)

    return df


def play_by_play(
    start_week: NflWeek, end_week: NflWeek, force_refresh: bool = False
) -> pd.DataFrame:
    """
    Get the play-by-play data for the given weeks.

    Parameters
    ----------
        start_week : NflWeek
            The start week to get data from (inclusive).
        end_week : NflWeek
            The end week to get data to (inclusive).
        force_refresh : bool
            If True, we automatically get the most up-to-date data from NFL Verse and overwrite the local file.
    """
    df = pd.concat(
        [
            _source_data.get("pbp", force_refresh, {"year": year})
            for year in range(start_week.season, end_week.season + 1)
        ]
    )
    df = utils.filter_data_weekly(df, start_week, end_week)

    return df
