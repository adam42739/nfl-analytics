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
        sorted(pd.concat((schedules["home_team"], schedules["away_team"])).unique())
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


def get_srs_breakdown(season: int, week: int) -> pd.DataFrame:
    """
    Get the Simple Rating System (SRS) breakdown for a given season and week.

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
    # Get the game IDs for this season up to the specified week
    schedules = nfl_data.get_schedules()
    schedules = utils.filter_data(
        schedules,
        start_week=NflWeek(season, 1),
        end_week=NflWeek(season, week),
    )
    game_ids = schedules["game_id"].unique()

    # Get the point breakdown data for each game up to the specified week
    point_breakdown = utils.get_point_breakdown(season)
    point_breakdown = point_breakdown[point_breakdown.index.isin(game_ids)]

    # Calculate the home field advantages
    hfa_o = (
        point_breakdown["home_offensive_points"].mean()
        - point_breakdown["away_offensive_points"].mean()
    )
    hfa_d = (
        point_breakdown["home_defensive_points"].mean()
        - point_breakdown["away_defensive_points"].mean()
    )
    hfa_st = (
        point_breakdown["home_special_teams_points"].mean()
        - point_breakdown["away_special_teams_points"].mean()
    )

    # Get the score differential equations for each game as ndarrays
    score_diff_eq1 = (
        point_breakdown["home_offensive_points"].to_numpy()
        - point_breakdown["away_defensive_points"].to_numpy()
        - hfa_o
    )
    score_diff_eq2 = (
        point_breakdown["away_offensive_points"].to_numpy()
        - point_breakdown["home_defensive_points"].to_numpy()
        + hfa_d
    )
    score_diff_eq3 = (
        point_breakdown["home_special_teams_points"].to_numpy()
        - point_breakdown["away_special_teams_points"].to_numpy()
        - hfa_st
    )
    score_diff = np.concatenate((score_diff_eq1, score_diff_eq2, score_diff_eq3))

    # Get the teams matrix
    #   - Team SRS breakdowns as columns: offensive, defense, then special teams, alphabetically from A to Z within a breakdown type
    #   - Games as rows (same index as score_diff): first eq1, then eq2, then eq3
    #   - values: 0, 1, or -1
    teams = pd.Series(
        sorted(pd.concat((schedules["home_team"], schedules["away_team"])).unique())
    )
    filler = np.zeros(len(score_diff_eq1))
    # The offensive breakdown: first 32 columns
    offensive_dict = {
        team
        + "_O": np.concatenate(
            (
                1 * (team == point_breakdown["home_team"]),
                1 * (team == point_breakdown["away_team"]),
                filler,
            )
        )
        for team in teams
    }
    # The defensive breakdown: next 32 columns
    defensive_dict = {
        team
        + "_D": np.concatenate(
            (
                -1 * (team == point_breakdown["away_team"]),
                -1 * (team == point_breakdown["home_team"]),
                filler,
            )
        )
        for team in teams
    }
    # The special teams breakdown: last 32 columns
    special_dict = {
        team
        + "_ST": np.concatenate(
            (
                filler,
                filler,
                1 * (team == point_breakdown["home_team"])
                + -1 * (team == point_breakdown["away_team"]),
            )
        )
        for team in teams
    }
    teams_df = pd.DataFrame({**offensive_dict, **defensive_dict, **special_dict})
    teams_matrix = teams_df.to_numpy()

    # Run least squares to get the SRS breakdown
    x, residuals, rank, s = np.linalg.lstsq(teams_matrix, score_diff, rcond=None)

    # Create the SRS DataFrame
    srs_df = pd.DataFrame(
        {
            "Team": teams,
            "SRS_O": x[:32],
            "SRS_D": x[32:64],
            "SRS_ST": x[64:],
            "SRS": x[:32] + x[32:64] + x[64:],
        }
    )

    # Ensure to normalize the SRS values so that the mean is 0
    srs_df["SRS_O"] = srs_df["SRS_O"] - srs_df["SRS_O"].mean()
    srs_df["SRS_D"] = srs_df["SRS_D"] - srs_df["SRS_D"].mean()
    srs_df["SRS_ST"] = srs_df["SRS_ST"] - srs_df["SRS_ST"].mean()

    return srs_df
