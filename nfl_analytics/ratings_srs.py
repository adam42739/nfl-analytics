from nfl_analytics import nfl_data
import pandas as pd
from nfl_analytics.nfl_data import NflWeek
import numpy as np


class RatingsSRS:
    """
    Simple Rating System (SRS) model for NFL teams.

    Includes SRS breakdown for offensive, defensive, and special teams ratings.
    """

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

        # Get a mask of games played at a neutral site, aligned with the point breakdown
        neutral_games = self._schedules.loc[
            self._schedules["location"] == "Neutral", "game_id"
        ]
        self._neutral_mask = self._point_breakdown.index.isin(neutral_games)

    def _calculate_hfa(self):
        """
        Calculate the home field advantage (HFA) for the given week.
        """
        # Offensive HFA
        home_points = self._point_breakdown.loc[
            ~self._neutral_mask, "home_offensive_points"
        ]
        away_points = self._point_breakdown.loc[
            ~self._neutral_mask, "away_offensive_points"
        ]
        self._hfa_o = home_points.mean() - away_points.mean()

        # Defensive HFA
        home_points = self._point_breakdown.loc[
            ~self._neutral_mask, "home_defensive_points"
        ]
        away_points = self._point_breakdown.loc[
            ~self._neutral_mask, "away_defensive_points"
        ]
        self._hfa_d = home_points.mean() - away_points.mean()

        # Special Teams HFA
        home_points = self._point_breakdown.loc[
            ~self._neutral_mask, "home_special_teams_points"
        ]
        away_points = self._point_breakdown.loc[
            ~self._neutral_mask, "away_special_teams_points"
        ]
        self._hfa_st = home_points.mean() - away_points.mean()

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
            - self._hfa_o * ~self._neutral_mask
        )

        # Defensive score differential
        self._score_diff_eq2 = (
            self._point_breakdown["away_offensive_points"].to_numpy()
            - self._point_breakdown["home_defensive_points"].to_numpy()
            + self._hfa_d * ~self._neutral_mask
        )

        # Special teams score differential
        self._score_diff_eq3 = (
            self._point_breakdown["home_special_teams_points"].to_numpy()
            - self._point_breakdown["away_special_teams_points"].to_numpy()
            - self._hfa_st * ~self._neutral_mask
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
