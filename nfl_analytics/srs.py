from nfl_analytics import nfl_data
import pandas as pd
from nfl_analytics import utils
from nfl_analytics.utils import NflWeek
import numpy as np


def get_srs(season: int, week: int) -> pd.DataFrame:
    """
    Get the Simple Rating System (SRS) for a given season and week.

    Parameters
    ----------
        season : int
            The NFL season year.
        week : int
            The week of the NFL season.

    Returns
    -------
        pd.DataFrame
    """
    # Get the schedules data for this season up to the specified week
    schedules = nfl_data.get_schedules()
    schedules = utils.filter_data(
        schedules,
        start_week=NflWeek(season, 1),
        end_week=NflWeek(season, week),
    )

    # Calculate the home field advantage
    hfa = schedules["home_score"].mean() - schedules["away_score"].mean()

    # Get the score differentials for each game as an ndarray
    score_diff = (
        schedules["home_score"].to_numpy() - schedules["away_score"].to_numpy() - hfa
    )

    # Get the teams matrix
    #   - Teams as columns alphabetically from A to Z
    #   - Games as rows (same index as score_diff)
    #   - 1 for home team, -1 for away team
    teams = pd.Series(
        sorted(
            np.concatenate(
                (schedules["home_team"].unique(), schedules["away_team"].unique())
            )
        )
    )
    teams_df = pd.DataFrame(
        {
            team: 1 * (team == schedules["home_team"])
            + -1 * (team == schedules["away_team"])
            for team in teams
        }
    )
    teams_matrix = teams_df.to_numpy()

    # Run least squares to get the SRS
    x, residuals, rank, s = np.linalg.lstsq(teams_matrix, score_diff, rcond=None)

    # Create the SRS DataFrame
    srs_df = pd.DataFrame(
        {
            "Team": teams,
            "SRS": x,
        }
    )

    return srs_df
