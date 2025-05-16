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


def filter_data(
    df: pd.DataFrame,
    after_week: NflWeek = NflWeek(1900, 1),
    before_week: NflWeek = NflWeek(2100, 1),
    season_col: str = "season",
    week_col: str = "week",
) -> pd.DataFrame:
    """
    Filter the DataFrame based on the given season and week range.

    Parameters
    ----------
        df : pd.DataFrame
            The DataFrame to filter.
        after_week : NflWeek
            The start week to filter from. Leave blank for no lower bound.
        before_week : NflWeek
            The end week to filter to. Leave blank for no upper bound.
        season_col : str
            The name of the column containing the season information. Default is "season".
        week_col : str
            The name of the column containing the week information. Default is "week".

    Returns
    -------
        pd.DataFrame
            The filtered DataFrame. Beware returned DataFrame is a slice.
    """
    return df[
        (df[season_col] >= after_week.season)
        & (df[season_col] <= before_week.season)
        & (df[week_col] >= after_week.week)
        & (df[week_col] <= before_week.week)
    ]
