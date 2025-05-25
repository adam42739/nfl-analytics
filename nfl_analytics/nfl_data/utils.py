import pandas as pd


class NflWeek:
    """
    A class to represent a week in the NFL season.
    """

    def __init__(self, season: int, week: int):
        self.season = season
        self.week = week

    def _update_const(self):
        """
        Update the instance constant variables.
        """
        self.season_start = NflWeek(self.season, 1)

    def _is_superbowl_week(self) -> bool:
        """
        Returns True if the week is the Super Bowl week, otherwise False.
        """
        if self.season >= 2021:
            return self.week == 22
        elif self.season >= 1994:
            return self.week == 21
        elif self.season >= 1993:
            return self.week == 22
        elif self.season >= 1990:
            return self.week == 21
        elif self.season >= 1978:
            return self.week == 20
        else:
            return self.week == 17

    def _advance_week(self):
        """
        Advance the week by one week.
        """
        if self._is_superbowl_week():
            self.season += 1
            self.week = 1
        else:
            self.week += 1

        self._update_const()

    def advance(self, weeks: int = 1):
        """
        Advance the week by a given number of weeks.
        """
        for _ in range(weeks):
            self._advance_week()

    def _go_back_week(self):
        """
        Back the week by one week.
        """
        if self.week == 1:
            if self.season >= 2021:
                self.week = 22
            elif self.season >= 1994:
                self.week = 21
            elif self.season >= 1993:
                self.week = 22
            elif self.season >= 1990:
                self.week = 21
            elif self.season >= 1978:
                self.week = 20
            else:
                self.week = 17
            self.season -= 1
        else:
            self.week -= 1

        self._update_const()

    def go_back(self, weeks: int = 1):
        """
        Back the week by a given number of weeks.
        """
        for _ in range(weeks):
            self._go_back_week()


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
