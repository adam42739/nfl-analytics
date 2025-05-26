import pandas as pd
from nfl_analytics.nfl_data import basic_data
from nfl_analytics.nfl_data.utils import NflWeek
import numpy as np


def point_breakdown(
    start_week: NflWeek, end_week: NflWeek, pbp_df: pd.DataFrame = None
) -> pd.DataFrame:
    """
    Get the point breakdown for each game during the given weeks.

    Parameters
    ----------
        start_week : NflWeek
            The start week to filter from (inclusive).
        end_week : NflWeek
            The end week to filter to (inclusive).
        pbp_df : pd.DataFrame, optional
            A DataFrame containing the play-by-play data for the given seasons.
            If not provided, it will be fetched.
            Useful for reducing IO calls when the data is already readily available.
    """
    # Get the play-by-play data for the given weeks if necessary
    if not isinstance(pbp_df, pd.DataFrame):
        pbp_df = basic_data.play_by_play(start_week, end_week)

    # Get only scoring plays and relevant columns
    pbp_df = pbp_df[pbp_df["sp"].astype(bool)]
    pbp_df = pbp_df[
        [
            "game_id",
            "home_team",
            "away_team",
            "posteam",
            "defteam",
            "posteam_score",
            "defteam_score",
            "posteam_score_post",
            "defteam_score_post",
            "special",
        ]
    ]
    pbp_df["special"] = pbp_df["special"].astype(bool)

    # =======================================================================
    # First we calculate the offensive points for each play
    # =======================================================================

    offensive_points = pbp_df["posteam_score_post"] - pbp_df["posteam_score"]

    # Get the home team offensive points
    home_team_possesion = pbp_df["posteam"] == pbp_df["home_team"]
    pbp_df["home_offensive_points"] = (
        home_team_possesion * ~pbp_df["special"] * offensive_points
    )

    # Get the away team offensive points
    away_team_possesion = pbp_df["posteam"] == pbp_df["away_team"]
    pbp_df["away_offensive_points"] = (
        away_team_possesion * ~pbp_df["special"] * offensive_points
    )
    # =======================================================================
    # Now we calculate the defensive points for each play
    # =======================================================================

    defensive_points = pbp_df["defteam_score_post"] - pbp_df["defteam_score"]

    # Get the home team defensive points
    home_team_defense = pbp_df["defteam"] == pbp_df["home_team"]
    pbp_df["home_defensive_points"] = (
        home_team_defense * ~pbp_df["special"] * defensive_points
    )

    # Get the away team defensive points
    away_team_defense = pbp_df["defteam"] == pbp_df["away_team"]
    pbp_df["away_defensive_points"] = (
        away_team_defense * ~pbp_df["special"] * defensive_points
    )

    # =======================================================================
    # Lastly we calculate the special teams points for each play
    # =======================================================================

    # Get the home team special teams points
    offensive_special_points = (
        home_team_possesion * pbp_df["special"] * offensive_points
    )
    defensive_special_points = home_team_defense * pbp_df["special"] * defensive_points
    pbp_df["home_special_teams_points"] = (
        offensive_special_points + defensive_special_points
    )

    # Get the away team special teams points
    offensive_special_points = (
        away_team_possesion * pbp_df["special"] * offensive_points
    )
    defensive_special_points = away_team_defense * pbp_df["special"] * defensive_points
    pbp_df["away_special_teams_points"] = (
        offensive_special_points + defensive_special_points
    )

    # =======================================================================

    # Get the home and way team scoring breakdown for each game
    point_breakdown = pbp_df.groupby("game_id").agg(
        {
            "home_team": "first",
            "away_team": "first",
            "home_offensive_points": "sum",
            "away_offensive_points": "sum",
            "home_defensive_points": "sum",
            "away_defensive_points": "sum",
            "home_special_teams_points": "sum",
            "away_special_teams_points": "sum",
        }
    )

    return point_breakdown


def margin_of_victory(
    start_week: NflWeek, end_week: NflWeek, schedules_df: pd.DataFrame = None
) -> pd.DataFrame:
    """
    Get the margin of victory (MoV) for each game in a given week.

    Parameters
    ----------
        start_week : NflWeek
            The start week to filter from (inclusive).
        end_week : NflWeek
            The end week to filter to (inclusive).
        schedules_df : pd.DataFrame, optional
            A DataFrame containing the schedule data for the given seasons.
            If not provided, it will be fetched.
            Useful for reducing IO calls when the data is already readily available.
    """
    # Get the schedule data for the given weeks if necessary
    if not isinstance(schedules_df, pd.DataFrame):
        schedules_df = basic_data.schedules(start_week, end_week)

    # Get each team's total points scored
    points_home = schedules_df.groupby("home_team")["home_score"].agg(["sum", "count"])
    points_away = schedules_df.groupby("away_team")["away_score"].agg(["sum", "count"])
    points_scored = points_home.add(points_away, fill_value=0)

    # Get each team's total points allowed
    points_home = schedules_df.groupby("home_team")["away_score"].agg(["sum", "count"])
    points_away = schedules_df.groupby("away_team")["home_score"].agg(["sum", "count"])
    points_allowed = points_home.add(points_away, fill_value=0)

    # Calculate the MOV
    mov = (points_scored["sum"] - points_allowed["sum"]) / points_scored["count"]
    mov.name = "MoV"
    mov.index.name = "Team"
    mov = mov.reset_index()
    mov = mov.sort_values(by="Team")

    return mov


def home_field_advantage(
    start_week: NflWeek,
    end_week: NflWeek,
    schedules_df: pd.DataFrame = None,
    point_breakdown_df: pd.DataFrame = None,
) -> tuple[float, float, float, float]:
    """
    Get the home field advantage (HFA) for each team in a given week.

    Parameters
    ----------
        start_week : NflWeek
            The start week to filter from (inclusive).
        end_week : NflWeek
            The end week to filter to (inclusive).
        point_breakdown_df : pd.DataFrame, optional
            A DataFrame containing the point breakdown data for the given seasons.
            If not provided, it will be fetched.
            Useful for reducing IO calls when the data is already readily available.

    Returns
    -------
        hfa, hfa_o, hfa_d, hfa_st : tuple[float, float, float, float]
    """
    # Get the schedule data for the given weeks if necessary
    if not isinstance(schedules_df, pd.DataFrame):
        schedules_df = basic_data.schedules(start_week, end_week)

    # Get the point breakdown data for the given weeks if necessary
    if not isinstance(point_breakdown_df, pd.DataFrame):
        point_breakdown_df = point_breakdown(start_week, end_week)

    # Create a mask for neutral site games
    neutral_game_ids = schedules_df.loc[
        schedules_df["location"] == "Neutral", "game_id"
    ]
    neutral_mask = point_breakdown_df.index.isin(neutral_game_ids)

    # Offensive HFA
    home_points = point_breakdown_df.loc[~neutral_mask, "home_offensive_points"]
    away_points = point_breakdown_df.loc[~neutral_mask, "away_offensive_points"]
    hfa_o = float(home_points.mean() - away_points.mean())

    # Defensive HFA
    home_points = point_breakdown_df.loc[~neutral_mask, "home_defensive_points"]
    away_points = point_breakdown_df.loc[~neutral_mask, "away_defensive_points"]
    hfa_d = float(home_points.mean() - away_points.mean())

    # Special Teams HFA
    home_points = point_breakdown_df.loc[~neutral_mask, "home_special_teams_points"]
    away_points = point_breakdown_df.loc[~neutral_mask, "away_special_teams_points"]
    hfa_st = float(home_points.mean() - away_points.mean())

    # Calculate the overall HFA
    hfa = hfa_o + hfa_d + hfa_st

    return hfa, hfa_o, hfa_d, hfa_st
