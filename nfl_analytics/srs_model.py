import pandas as pd
import numpy as np
from nfl_analytics.nfl_data import NflWeek
from nfl_analytics import nfl_data


class _SrsFitter:
    def __init__(self, start_week: NflWeek, end_week: NflWeek):
        """
        Initialize the SRS fitter with the start and end weeks.

        Parameters
        ----------
            start_week : NflWeek
                The start week of the season (inclusive).
            end_week : NflWeek
                The end week of the season (inclusive).
        """
        self.start_week = start_week
        self.end_week = end_week

    def fit(self):
        self._get_data()
        self._calculate_score_diff()
        self._setup_teams_matrix()
        self._solve_least_squares()
        self._create_srs_frame()
        self._normalize_srs()

    def _get_data(self):
        """
        Get the relevant computational data for the SRS.
        """
        self._schedules_df = nfl_data.schedules(self.start_week, self.end_week)
        self._point_breakdown_df = nfl_data.point_breakdown(
            self.start_week, self.end_week
        )
        self._hfa, self._hfa_o, self._hfa_d, self._hfa_st = (
            nfl_data.home_field_advantage(
                self.start_week,
                self.end_week,
                self._schedules_df,
                self._point_breakdown_df,
            )
        )

        # Get a mask of games played at a neutral site, aligned with the point breakdown
        neutral_games = self._schedules_df.loc[
            self._schedules_df["location"] == "Neutral", "game_id"
        ]
        self._neutral_mask = self._point_breakdown_df.index.isin(neutral_games)

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
            self._point_breakdown_df["home_offensive_points"].to_numpy()
            - self._point_breakdown_df["away_defensive_points"].to_numpy()
            - self._hfa_o * ~self._neutral_mask
        )

        # Defensive score differential
        self._score_diff_eq2 = (
            self._point_breakdown_df["away_offensive_points"].to_numpy()
            - self._point_breakdown_df["home_defensive_points"].to_numpy()
            + self._hfa_d * ~self._neutral_mask
        )

        # Special teams score differential
        self._score_diff_eq3 = (
            self._point_breakdown_df["home_special_teams_points"].to_numpy()
            - self._point_breakdown_df["away_special_teams_points"].to_numpy()
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
                    (self._schedules_df["home_team"], self._schedules_df["away_team"])
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
                    1 * (team == self._point_breakdown_df["home_team"]),
                    1 * (team == self._point_breakdown_df["away_team"]),
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
                    -1 * (team == self._point_breakdown_df["away_team"]),
                    -1 * (team == self._point_breakdown_df["home_team"]),
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
                    1 * (team == self._point_breakdown_df["home_team"])
                    + -1 * (team == self._point_breakdown_df["away_team"]),
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
        mov = nfl_data.margin_of_victory(
            self.start_week, self.end_week, self._schedules_df
        )
        srs = self._x[:32] + self._x[32:64] + self._x[64:]
        sos = srs - mov["MoV"].to_numpy()

        # Create the SRS DataFrame
        self.srs_frame = pd.DataFrame(
            {
                "Team": pd.Series(
                    sorted(
                        pd.concat(
                            (
                                self._schedules_df["home_team"],
                                self._schedules_df["away_team"],
                            )
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


class _SrsPredictor:
    def __init__(self, fitter: _SrsFitter):
        self._srs_frame = fitter.srs_frame
        self._hfa = fitter._hfa
        self._hfa_o = fitter._hfa_o
        self._hfa_d = fitter._hfa_d
        self._hfa_st = fitter._hfa_st

    def predict(self, games: pd.DataFrame) -> pd.DataFrame:
        """
        Predict the spreads for a given schedule.

        Parameters
        ----------
        games : pd.DataFrame
            A DataFrame containing the game schedule with columns:
            - 'game_id': Unique identifier for the game
            - 'home_team': Abbreviation of the home team
            - 'away_team': Abbreviation of the away team
            - 'is_neutral': Boolean indicating if the game is played at a neutral site

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the predicted spreads for each game in the schedule.
        """
        self._games = games.copy()

        self._merge_srs_data()
        self._predict_spreads()

        return self._games

    def _merge_srs_data(self):
        """
        Merge home and away team SRS data into the games DataFrame.
        """
        # Merge home team SRS data
        self._games = pd.merge(
            self._games,
            self._srs_frame[["Team", "SRS", "SRS_O", "SRS_D", "SRS_ST"]].rename(
                {
                    "SRS": "SRS_home",
                    "SRS_O": "SRS_O_home",
                    "SRS_D": "SRS_D_home",
                    "SRS_ST": "SRS_ST_home",
                },
                axis="columns",
            ),
            left_on="home_team",
            right_on="Team",
            how="left",
        ).drop(columns=["Team"])

        # Merge away team SRS data
        self._games = pd.merge(
            self._games,
            self._srs_frame[["Team", "SRS", "SRS_O", "SRS_D", "SRS_ST"]].rename(
                {
                    "SRS": "SRS_away",
                    "SRS_O": "SRS_O_away",
                    "SRS_D": "SRS_D_away",
                    "SRS_ST": "SRS_ST_away",
                },
                axis="columns",
            ),
            left_on="away_team",
            right_on="Team",
            how="left",
        ).drop(columns=["Team"])

    def _predict_spreads(self):
        """
        Predict the game spreads based on the SRS values and home field advantage.
        """
        # Overal game spreads
        self._games["pred_spread"] = (
            self._games["SRS_home"]
            - self._games["SRS_away"]
            + self._hfa * ~self._games["is_neutral"]
        )

        # Offensive component of the spread
        self._games["pred_spread_O"] = (
            self._games["SRS_O_home"]
            - self._games["SRS_O_away"]
            + self._hfa_o * ~self._games["is_neutral"]
        )

        # Defensive component of the spread
        self._games["pred_spread_D"] = (
            self._games["SRS_D_home"]
            - self._games["SRS_D_away"]
            + self._hfa_d * ~self._games["is_neutral"]
        )

        # Special teams component of the spread
        self._games["pred_spread_ST"] = (
            self._games["SRS_ST_home"]
            - self._games["SRS_ST_away"]
            + self._hfa_st * ~self._games["is_neutral"]
        )

        # Drop unnecessary columns
        self._games = self._games.drop(
            columns=[
                "is_neutral",
                "SRS_home",
                "SRS_away",
                "SRS_O_home",
                "SRS_O_away",
                "SRS_D_home",
                "SRS_D_away",
                "SRS_ST_home",
                "SRS_ST_away",
            ]
        )


class SrsModel:
    def __init__(self, start_week: NflWeek, end_week: NflWeek):
        """
        Initialize the SRS model with the start and end weeks.

        Parameters
        ----------
            start_week : NflWeek
                The start week of the season (inclusive).
            end_week : NflWeek
                The end week of the season (inclusive).
        """
        self._fitter = _SrsFitter(start_week, end_week)
        self._fitter.fit()

        self._predictor = _SrsPredictor(self._fitter)

    def predict(self, games: pd.DataFrame) -> pd.DataFrame:
        """
        Predict the spreads for a given schedule.

        Parameters
        ----------
        games : pd.DataFrame
            A DataFrame containing the game schedule with columns:
            - 'game_id': Unique identifier for the game
            - 'home_team': Abbreviation of the home team
            - 'away_team': Abbreviation of the away team
            - 'is_neutral': Boolean indicating if the game is played at a neutral site

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the predicted spreads for each game in the schedule.
        """
        return self._predictor.predict(games)