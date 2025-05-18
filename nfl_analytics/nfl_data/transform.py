import pandas as pd
from nfl_analytics.nfl_data import sourcing
from nfl_analytics.nfl_data.utils import NflWeek


def filter_data(
    df: pd.DataFrame,
    start_week: NflWeek = NflWeek(1900, 1),
    end_week: NflWeek = NflWeek(2100, 1),
    season_col: str = "season",
    week_col: str = "week",
) -> pd.DataFrame:
    """
    Filter the DataFrame based on the given season and week range.

    Parameters
    ----------
        df : pd.DataFrame
            The DataFrame to filter.
        start_week : NflWeek
            The start week to filter from (inclusive). Leave blank for no lower bound.
        end_week : NflWeek
            The end week to filter to (inclusive). Leave blank for no upper bound.
        season_col : str
            The name of the column containing the season information. Default is "season".
        week_col : str
            The name of the column containing the week information. Default is "week".

    Returns
    -------
        pd.DataFrame
            The filtered DataFrame. Beware returned DataFrame is a slice.
    """
    # Filter the DataFrame by the given season
    start_mask = df[season_col] >= start_week.season
    end_mask = df[season_col] <= end_week.season
    df = df[start_mask & end_mask]

    # Filter the DataFrame by the given week
    lower_edge_mask = df[season_col] == start_week.season
    start_mask = ~lower_edge_mask | (df[week_col] >= start_week.week)
    upper_edge_mask = df[season_col] == end_week.season
    end_mask = ~upper_edge_mask | (df[week_col] <= end_week.week)
    df = df[start_mask & end_mask]

    return df


def point_breakdown(season: int) -> pd.DataFrame:
    """
    Get the point breakdown (offensive vs. special teams points) for each game.
    Scoring breakdown is sourced from the play-by-play data.

    Parameters
    ----------
        season : int
            The NFL season year.

    Returns
    -------
        pd.DataFrame
            The point breakdown for each play.
    """
    # Get the play-by-play data for the given season
    pbp_df = sourcing.get_pbp(season)

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


def calc_mov(week: NflWeek) -> pd.DataFrame:
    """
    Get the margin of victory (MOV) for each game in a given week.

    Parameters
    ----------
        week : NflWeek
            The current week of the NFL season.

    Returns
    -------
        pd.DataFrame
            The MOV by team.
    """
    # Get the schedule data for the given week
    schedules = sourcing.get_schedules()
    schedules = filter_data(
        schedules,
        start_week=NflWeek(week.season, 1),
        end_week=week,
    )

    # Get each team's total points scored
    points_home = schedules.groupby("home_team")["home_score"].agg(["sum", "count"])
    points_away = schedules.groupby("away_team")["away_score"].agg(["sum", "count"])
    points_scored = points_home.add(points_away, fill_value=0)

    # Get each team's total points allowed
    points_home = schedules.groupby("home_team")["away_score"].agg(["sum", "count"])
    points_away = schedules.groupby("away_team")["home_score"].agg(["sum", "count"])
    points_allowed = points_home.add(points_away, fill_value=0)

    # Calculate the MOV
    mov = (points_scored["sum"] - points_allowed["sum"]) / points_scored["count"]
    mov.name = "MoV"
    mov.index.name = "Team"
    mov = mov.reset_index()
    mov = mov.sort_values(by="Team")

    return mov
