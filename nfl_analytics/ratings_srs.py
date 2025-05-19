from nfl_analytics import nfl_data
import pandas as pd
from nfl_analytics.nfl_data import NflWeek
import numpy as np
from dataclasses import dataclass


@dataclass
class _RatingsSRSFitData:
    """
    Data class to hold the data used in the SRS fitting process.
    """

    schedules: pd.DataFrame = None
    point_breakdown: pd.DataFrame = None
    game_ids: np.ndarray = None
    neutral_mask: np.ndarray = None
    score_diff_eq1: np.ndarray = None
    score_diff_eq2: np.ndarray = None
    score_diff_eq3: np.ndarray = None
    score_diff: np.ndarray = None
    teams_matrix: np.ndarray = None
    x: np.ndarray = None
    residuals: np.ndarray = None
    rank: int = None
    s: np.ndarray = None


@dataclass
class _RatingsSRSPredictScheduleData:
    """
    Data class to hold the data used in the SRS prediction process.
    """

    start_week: NflWeek = None
    end_week: NflWeek = None
    games: pd.DataFrame = None


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
        self._data = _RatingsSRSFitData()

        self._fit_get_data()
        self._fit_calculate_hfa()
        self._fit_calculate_score_diff()
        self._fit_setup_teams_matrix()
        self._fit_solve_least_squares()
        self._fit_create_srs_frame()
        self._fit_normalize_srs()

        del self._data

    def _fit_get_data(self):
        """
        Get the relevant computational data for the SRS.
        """
        # Get the schedules data and game IDs for this season up to the specified week
        self._data.schedules = nfl_data.get_schedules()
        self._data.schedules = nfl_data.filter_data(
            self._data.schedules,
            start_week=NflWeek(self.week.season, 1),
            end_week=self.week,
        )
        self._data.game_ids = self._data.schedules["game_id"].unique()

        # Get the point breakdown data for each game up to the specified week
        self._data.point_breakdown = nfl_data.get_point_breakdown(self.week.season)
        self._data.point_breakdown = self._data.point_breakdown[
            self._data.point_breakdown.index.isin(self._data.game_ids)
        ]

        # Get a mask of games played at a neutral site, aligned with the point breakdown
        neutral_games = self._data.schedules.loc[
            self._data.schedules["location"] == "Neutral", "game_id"
        ]
        self._data.neutral_mask = self._data.point_breakdown.index.isin(neutral_games)

    def _fit_calculate_hfa(self):
        """
        Calculate the home field advantage (HFA) for the given week.
        """
        # Offensive HFA
        home_points = self._data.point_breakdown.loc[
            ~self._data.neutral_mask, "home_offensive_points"
        ]
        away_points = self._data.point_breakdown.loc[
            ~self._data.neutral_mask, "away_offensive_points"
        ]
        self._hfa_o = home_points.mean() - away_points.mean()

        # Defensive HFA
        home_points = self._data.point_breakdown.loc[
            ~self._data.neutral_mask, "home_defensive_points"
        ]
        away_points = self._data.point_breakdown.loc[
            ~self._data.neutral_mask, "away_defensive_points"
        ]
        self._hfa_d = home_points.mean() - away_points.mean()

        # Special Teams HFA
        home_points = self._data.point_breakdown.loc[
            ~self._data.neutral_mask, "home_special_teams_points"
        ]
        away_points = self._data.point_breakdown.loc[
            ~self._data.neutral_mask, "away_special_teams_points"
        ]
        self._hfa_st = home_points.mean() - away_points.mean()

        # Calculate the overall HFA
        self._hfa = self._hfa_o + self._hfa_d + self._hfa_st

    def _fit_calculate_score_diff(self):
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
        self._data.score_diff_eq1 = (
            self._data.point_breakdown["home_offensive_points"].to_numpy()
            - self._data.point_breakdown["away_defensive_points"].to_numpy()
            - self._hfa_o * ~self._data.neutral_mask
        )

        # Defensive score differential
        self._data.score_diff_eq2 = (
            self._data.point_breakdown["away_offensive_points"].to_numpy()
            - self._data.point_breakdown["home_defensive_points"].to_numpy()
            + self._hfa_d * ~self._data.neutral_mask
        )

        # Special teams score differential
        self._data.score_diff_eq3 = (
            self._data.point_breakdown["home_special_teams_points"].to_numpy()
            - self._data.point_breakdown["away_special_teams_points"].to_numpy()
            - self._hfa_st * ~self._data.neutral_mask
        )

        # Concatenate the score differentials
        self._data.score_diff = np.concatenate(
            (
                self._data.score_diff_eq1,
                self._data.score_diff_eq2,
                self._data.score_diff_eq3,
            )
        )

    def _fit_setup_teams_matrix(self):
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
                    (
                        self._data.schedules["home_team"],
                        self._data.schedules["away_team"],
                    )
                ).unique()
            )
        )

        # Create a filler array of zeros (length = number of games)
        filler = np.zeros(len(self._data.score_diff_eq1))

        # The offensive breakdown: first 32 columns
        offensive_dict = {
            team
            + "_O": np.concatenate(
                (
                    1 * (team == self._data.point_breakdown["home_team"]),
                    1 * (team == self._data.point_breakdown["away_team"]),
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
                    -1 * (team == self._data.point_breakdown["away_team"]),
                    -1 * (team == self._data.point_breakdown["home_team"]),
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
                    1 * (team == self._data.point_breakdown["home_team"])
                    + -1 * (team == self._data.point_breakdown["away_team"]),
                )
            )
            for team in teams
        }

        # Combine all dictionaries into a single DataFrame
        teams_df = pd.DataFrame({**offensive_dict, **defensive_dict, **special_dict})
        self._data.teams_matrix = teams_df.to_numpy()

    def _fit_solve_least_squares(self):
        """
        Solve the least squares problem to get the SRS values.
        """
        # Run least squares to get the SRS
        (
            self._data.x,
            self._data.residuals,
            self._data.rank,
            self._data.s,
        ) = np.linalg.lstsq(self._data.teams_matrix, self._data.score_diff, rcond=None)

    def _fit_create_srs_frame(self):
        """
        Create the SRS DataFrame.
        """
        # Calculate the MoV and SoS for each team
        mov = nfl_data.get_margin_of_victory(NflWeek(self.week.season, 1), self.week)
        srs = self._data.x[:32] + self._data.x[32:64] + self._data.x[64:]
        sos = srs - mov["MoV"].to_numpy()

        # Create the SRS DataFrame
        self.srs_frame = pd.DataFrame(
            {
                "Team": pd.Series(
                    sorted(
                        pd.concat(
                            (
                                self._data.schedules["home_team"],
                                self._data.schedules["away_team"],
                            )
                        ).unique()
                    )
                ),
                "MoV": mov["MoV"],
                "SoS": sos,
                "SRS": srs,
                "SRS_O": self._data.x[:32],
                "SRS_D": self._data.x[32:64],
                "SRS_ST": self._data.x[64:],
            }
        )

    def _fit_normalize_srs(self):
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

    def predict_game(
        self, home_team: str, away_team: str, is_neutral: bool = False
    ) -> dict[str, float]:
        """
        Predict the spread differential for a given matchup.

        Parameters
        ----------
        home_team : str
            The home team.
        away_team : str
            The away team.
        is_neutral : bool, optional
            Whether the game is at a neutral site (default is False).

        Returns
        -------
        dict[str, float]
            A dictionary containing the predicted spreads for the matchup.
            Keys are:
            - "spread": The predicted spread.
            - "offensive": The predicted offensive componenet of the spread.
            - "defensive": The predicted defensive component of the spread.
            - "special": The predicted special teams component of the spread.
        """
        # Get the SRS values for the teams
        home_srs = self.srs_frame.loc[
            self.srs_frame["Team"] == home_team, "SRS"
        ].values[0]
        home_srs_o = self.srs_frame.loc[
            self.srs_frame["Team"] == home_team, "SRS_O"
        ].values[0]
        home_srs_d = self.srs_frame.loc[
            self.srs_frame["Team"] == home_team, "SRS_D"
        ].values[0]
        home_srs_st = self.srs_frame.loc[
            self.srs_frame["Team"] == home_team, "SRS_ST"
        ].values[0]
        away_srs = self.srs_frame.loc[
            self.srs_frame["Team"] == away_team, "SRS"
        ].values[0]
        away_srs_o = self.srs_frame.loc[
            self.srs_frame["Team"] == away_team, "SRS_O"
        ].values[0]
        away_srs_d = self.srs_frame.loc[
            self.srs_frame["Team"] == away_team, "SRS_D"
        ].values[0]
        away_srs_st = self.srs_frame.loc[
            self.srs_frame["Team"] == away_team, "SRS_ST"
        ].values[0]

        # Calculate the predicted spreads
        spread = float(home_srs - away_srs + self._hfa * (not is_neutral))
        spread_o = float(home_srs_o - away_srs_d + self._hfa_o * (not is_neutral))
        spread_d = float(home_srs_d - away_srs_o + self._hfa_d * (not is_neutral))
        spread_st = float(home_srs_st - away_srs_st + self._hfa_st * (not is_neutral))

        # Return a simple dictionary with the spreads
        return {
            "spread": spread,
            "offensive": spread_o,
            "defensive": spread_d,
            "special": spread_st,
        }

    def predict_schedule(self, start_week: NflWeek, end_week: NflWeek) -> pd.DataFrame:
        """
        Predict the spreads for a given schedule.

        Parameters
        ----------
        start_week : NflWeek
            The start week of the schedule (inclusive).
        end_week : NflWeek
            The end week of the schedule (inclusive).

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the predicted spreads for each game in the schedule.
        """
        self._data = _RatingsSRSPredictScheduleData(
            start_week=start_week, end_week=end_week
        )

        self._predict_schedule_get_data()
        self._predict_schedule_merge_srs()
        self._predict_schedule_predict_spreads()
        self._predict_schedule_actual_spreads()

        return_frame = self._data.games.copy()

        del self._data

        return return_frame

    def _predict_schedule_get_data(self):
        """
        Get the relevant data for the SRS prediction process.
        """
        # Get the games data for the specified weeks
        schedules = nfl_data.get_schedules()
        self._data.games = nfl_data.filter_data(
            schedules,
            self._data.start_week,
            self._data.end_week,
        )[["game_id", "location"]]
        self._data.games["is_neutral"] = self._data.games["location"] == "Neutral"
        self._data.games = self._data.games.drop(columns=["location"])

        # Get the point breakdown data for each game
        point_breakdown = pd.concat(
            [
                nfl_data.get_point_breakdown(season)
                for season in range(
                    self._data.start_week.season,
                    self._data.end_week.season + 1,
                )
            ]
        )
        self._data.games = pd.merge(
            self._data.games, point_breakdown, on="game_id", how="left"
        )

    def _predict_schedule_merge_srs(self):
        """
        Merge the SRS data with the games data.
        """
        # Merge home team SRS data
        self._data.games = pd.merge(
            self._data.games,
            self.srs_frame[["Team", "SRS", "SRS_O", "SRS_D", "SRS_ST"]].rename(
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
        self._data.games = pd.merge(
            self._data.games,
            self.srs_frame[["Team", "SRS", "SRS_O", "SRS_D", "SRS_ST"]].rename(
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

    def _predict_schedule_predict_spreads(self):
        """
        Calculate the predicted spreads for each game in the schedule.
        """
        # Overal game spreads
        self._data.games["pred_spread"] = (
            self._data.games["SRS_home"]
            - self._data.games["SRS_away"]
            + self._hfa * ~self._data.games["is_neutral"]
        )

        # Offensive component of the spread
        self._data.games["pred_spread_O"] = (
            self._data.games["SRS_O_home"]
            - self._data.games["SRS_O_away"]
            + self._hfa_o * ~self._data.games["is_neutral"]
        )

        # Defensive component of the spread
        self._data.games["pred_spread_D"] = (
            self._data.games["SRS_D_home"]
            - self._data.games["SRS_D_away"]
            + self._hfa_d * ~self._data.games["is_neutral"]
        )

        # Special teams component of the spread
        self._data.games["pred_spread_ST"] = (
            self._data.games["SRS_ST_home"]
            - self._data.games["SRS_ST_away"]
            + self._hfa_st * ~self._data.games["is_neutral"]
        )

        # Drop unnecessary columns
        self._data.games = self._data.games.drop(
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

    def _predict_schedule_actual_spreads(self):
        """
        Calculate the actual spreads for each game in the schedule.
        """
        # Offensive component of the spread
        self._data.games["spread_O"] = (
            self._data.games["home_offensive_points"]
            - self._data.games["away_offensive_points"]
        )

        # Defensive component of the spread
        self._data.games["spread_D"] = (
            self._data.games["home_defensive_points"]
            - self._data.games["away_defensive_points"]
        )

        # Special teams component of the spread
        self._data.games["spread_ST"] = (
            self._data.games["home_special_teams_points"]
            - self._data.games["away_special_teams_points"]
        )

        # Overall game spread
        self._data.games["spread"] = (
            self._data.games["spread_O"]
            + self._data.games["spread_D"]
            + self._data.games["spread_ST"]
        )
