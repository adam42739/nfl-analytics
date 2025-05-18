from nfl_analytics import nfl_data
import pandas as pd
from nfl_analytics.nfl_data import NflWeek
import numpy as np


def get_srs(week: NflWeek) -> pd.DataFrame:
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
    schedules = nfl_data.filter_data(
        schedules,
        start_week=NflWeek(week.season, 1),
        end_week=week,
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

    # Calculate the MoV and SoS for each team
    mov = nfl_data.get_margin_of_victory(NflWeek(week.season, 1), week)
    sos = x - mov["MoV"].to_numpy()

    # Create the SRS DataFrame
    srs_df = pd.DataFrame(
        {
            "Team": teams,
            "MoV": mov["MoV"],
            "SoS": sos,
            "SRS": x,
        }
    )

    return srs_df


class RatingsSRS:
    def __init__(self, week: NflWeek):
        self.week = week

    def fit(self):
        """
        Fit the SRS model to the data for the given week using least squares.
        """
        self._get_data()
        self._calculate_hfa()
        self._calculate_score_diff()
        self._setup_teams_matrix()
        self._solve_least_squares()
        self._create_srs_frame()
        self._normalize_srs()

    def _get_data(self):
        """
        Get the relevant computational data for the SRS.
        """
        # Get the schedules data and game IDs for this season up to the specified week
        self._schedules = nfl_data.get_schedules()
        self._schedules = nfl_data.filter_data(
            self._schedules,
            start_week=NflWeek(self.week.season, 1),
            end_week=self.week,
        )
        self._game_ids = self._schedules["game_id"].unique()

        # Get the point breakdown data for each game up to the specified week
        self._point_breakdown = nfl_data.get_point_breakdown(self.week.season)
        self._point_breakdown = self._point_breakdown[
            self._point_breakdown.index.isin(self._game_ids)
        ]

    def _calculate_hfa(self):
        """
        Calculate the home field advantage (HFA) for the given week.
        """
        # Offensive HFA
        self._hfa_o = (
            self._point_breakdown["home_offensive_points"].mean()
            - self._point_breakdown["away_offensive_points"].mean()
        )

        # Defensive HFA
        self._hfa_d = (
            self._point_breakdown["home_defensive_points"].mean()
            - self._point_breakdown["away_defensive_points"].mean()
        )

        # Special Teams HFA
        self._hfa_st = (
            self._point_breakdown["home_special_teams_points"].mean()
            - self._point_breakdown["away_special_teams_points"].mean()
        )

        # Calculate the overall HFA
        self._hfa = self._hfa_o + self._hfa_d + self._hfa_st

    def _calculate_score_diff(self):
        """
        Calculate the score differentials for each game.

        Refer to the paper for additional details.
        Overall least squares problem is set up as:

        ===================  =  =============  =============  =================
        Score Differentials  =  Offensive SRS  Defensive SRS  Special Teams SRS
        ===================  =  =============  =============  =================
        Offensive Points     =  +1 or 0        -1 or 0        0
        Defensive Points     =  -1 or 0        +1 or 0        0
        Special Teams Points =  0              0              +1 or 0 or -1
        """
        # Offensive score differential
        self._score_diff_eq1 = (
            self._point_breakdown["home_offensive_points"].to_numpy()
            - self._point_breakdown["away_defensive_points"].to_numpy()
            - self._hfa_o
        )

        # Defensive score differential
        self._score_diff_eq2 = (
            self._point_breakdown["away_offensive_points"].to_numpy()
            - self._point_breakdown["home_defensive_points"].to_numpy()
            + self._hfa_d
        )

        # Special teams score differential
        self._score_diff_eq3 = (
            self._point_breakdown["home_special_teams_points"].to_numpy()
            - self._point_breakdown["away_special_teams_points"].to_numpy()
            - self._hfa_st
        )

        # Concatenate the score differentials
        self._score_diff = np.concatenate(
            (self._score_diff_eq1, self._score_diff_eq2, self._score_diff_eq3)
        )

    def _setup_teams_matrix(self):
        """
        Set up the teams matrix for the SRS calculation.

        Refer to the paper for additional details.
        Overall least squares problem is set up as:

        ===================  =  =============  =============  =================
        Score Differentials  =  Offensive SRS  Defensive SRS  Special Teams SRS
        ===================  =  =============  =============  =================
        Offensive Points     =  +1 or 0        -1 or 0        0
        Defensive Points     =  -1 or 0        +1 or 0        0
        Special Teams Points =  0              0              +1 or 0 or -1
        """
        # Get all teams alphabetically from A to Z
        teams = pd.Series(
            sorted(
                pd.concat(
                    (self._schedules["home_team"], self._schedules["away_team"])
                ).unique()
            )
        )

        # Create a filler array of zeros (length = number of games)
        filler = np.zeros(len(self._score_diff_eq1))

        # The offensive breakdown: first 32 columns
        offensive_dict = {
            team
            + "_O": np.concatenate(
                (
                    1 * (team == self._point_breakdown["home_team"]),
                    1 * (team == self._point_breakdown["away_team"]),
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
                    -1 * (team == self._point_breakdown["away_team"]),
                    -1 * (team == self._point_breakdown["home_team"]),
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
                    1 * (team == self._point_breakdown["home_team"])
                    + -1 * (team == self._point_breakdown["away_team"]),
                )
            )
            for team in teams
        }

        # Combine all dictionaries into a single DataFrame
        teams_df = pd.DataFrame({**offensive_dict, **defensive_dict, **special_dict})
        self._teams_matrix = teams_df.to_numpy()

    def _solve_least_squares(self):
        """
        Solve the least squares problem to get the SRS values.
        """
        # Run least squares to get the SRS
        self._x, self._residuals, self._rank, self._s = np.linalg.lstsq(
            self._teams_matrix, self._score_diff, rcond=None
        )

    def _create_srs_frame(self):
        """
        Create the SRS DataFrame.
        """
        # Calculate the MoV and SoS for each team
        mov = nfl_data.get_margin_of_victory(NflWeek(self.week.season, 1), self.week)
        srs = self._x[:32] + self._x[32:64] + self._x[64:]
        sos = srs - mov["MoV"].to_numpy()

        # Create the SRS DataFrame
        self.srs_frame = pd.DataFrame(
            {
                "Team": pd.Series(
                    sorted(
                        pd.concat(
                            (self._schedules["home_team"], self._schedules["away_team"])
                        ).unique()
                    )
                ),
                "MoV": mov["MoV"],
                "SoS": sos,
                "SRS": srs,
                "SRS_O": self._x[:32],
                "SRS_D": self._x[32:64],
                "SRS_ST": self._x[64:],
            }
        )

    def _normalize_srs(self):
        """
        Normalize the SRS values so that the mean is 0.
        """
        self.srs_frame["SRS_O"] = (
            self.srs_frame["SRS_O"] - self.srs_frame["SRS_O"].mean()
        )
        self.srs_frame["SRS_D"] = (
            self.srs_frame["SRS_D"] - self.srs_frame["SRS_D"].mean()
        )
        self.srs_frame["SRS_ST"] = (
            self.srs_frame["SRS_ST"] - self.srs_frame["SRS_ST"].mean()
        )


def get_srs_breakdown(week: NflWeek) -> pd.DataFrame:
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
    schedules = nfl_data.filter_data(
        schedules,
        start_week=NflWeek(week.season, 1),
        end_week=week,
    )
    game_ids = schedules["game_id"].unique()

    # Get the point breakdown data for each game up to the specified week
    point_breakdown = nfl_data.get_point_breakdown(week.season)
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

    # Calculate the MOV and SoS for each team
    mov = nfl_data.get_margin_of_victory(NflWeek(week.season, 1), week)
    srs = x[:32] + x[32:64] + x[64:]
    sos = srs - mov["MoV"].to_numpy()

    # Create the SRS DataFrame
    srs_df = pd.DataFrame(
        {
            "Team": teams,
            "MoV": mov["MoV"],
            "SoS": sos,
            "SRS": srs,
            "SRS_O": x[:32],
            "SRS_D": x[32:64],
            "SRS_ST": x[64:],
        }
    )

    # Ensure to normalize the SRS values so that the mean is 0
    srs_df["SRS_O"] = srs_df["SRS_O"] - srs_df["SRS_O"].mean()
    srs_df["SRS_D"] = srs_df["SRS_D"] - srs_df["SRS_D"].mean()
    srs_df["SRS_ST"] = srs_df["SRS_ST"] - srs_df["SRS_ST"].mean()

    return srs_df
