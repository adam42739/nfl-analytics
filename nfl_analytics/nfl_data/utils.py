import pandas as pd


class NflWeek:
    """
    A class to represent a week in the NFL season.
    """

    def __init__(self, season: int, week: int):
        self.season = season
        self.week = week

    def __str__(self):
        return f"{self.season} Week {self.week}"

    def __repr__(self):
        return f"NflWeek(year={self.season}, week={self.week})"


def filter_data_weekly(
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


def filter_data_seasonaly(
    df: pd.DataFrame,
    start_season: int = 1900,
    end_season: int = 2100,
    season_col: str = "season",
) -> pd.DataFrame:
    """
    Filter the DataFrame based on the given season range.

    Parameters
    ----------
        df : pd.DataFrame
            The DataFrame to filter.
        start_season : int
            The start season to filter from (inclusive). Leave blank for no lower bound.
        end_season : int
            The end season to filter to (inclusive). Leave blank for no upper bound.
        season_col : str
            The name of the column containing the season information. Default is "season".

    Returns
    -------
        pd.DataFrame
            The filtered DataFrame. Beware returned DataFrame is a slice.
    """
    # Filter the DataFrame by the given season
    start_mask = df[season_col] >= start_season
    end_mask = df[season_col] <= end_season
    df = df[start_mask & end_mask]

    return df
