from nfl_analytics import srs_model
from nfl_analytics.nfl_data import NflWeek
import pandas as pd


def test_srs_fitter():
    # Get the SRS breakdown for the end of the 2024 season
    fitter = srs_model._SrsFitter(NflWeek(2024, 1), NflWeek(2024, 18))
    fitter.fit()
    srs_frame = (
        fitter.srs_frame.sort_values(by="SRS", ascending=False)
        .round(1)
        .reset_index(drop=True)
    )

    # The expected SRS results
    exepcted_srs = pd.DataFrame(
        [
            {
                "Team": "DET",
                "MoV": 13.1,
                "SoS": 0.7,
                "SRS": 13.8,
                "SRS_O": 9.8,
                "SRS_D": 2.1,
                "SRS_ST": 1.9,
            },
            {
                "Team": "BAL",
                "MoV": 9.2,
                "SoS": 0.6,
                "SRS": 9.9,
                "SRS_O": 7.8,
                "SRS_D": 0.6,
                "SRS_ST": 1.5,
            },
            {
                "Team": "GB",
                "MoV": 7.2,
                "SoS": 0.9,
                "SRS": 8.0,
                "SRS_O": 4.3,
                "SRS_D": 2.0,
                "SRS_ST": 1.8,
            },
            {
                "Team": "BUF",
                "MoV": 9.2,
                "SoS": -1.2,
                "SRS": 8.0,
                "SRS_O": 7.8,
                "SRS_D": -0.0,
                "SRS_ST": 0.3,
            },
            {
                "Team": "PHI",
                "MoV": 9.4,
                "SoS": -1.6,
                "SRS": 7.8,
                "SRS_O": 3.2,
                "SRS_D": 2.6,
                "SRS_ST": 2.0,
            },
            {
                "Team": "TB",
                "MoV": 6.9,
                "SoS": -0.4,
                "SRS": 6.5,
                "SRS_O": 5.3,
                "SRS_D": 0.7,
                "SRS_ST": 0.4,
            },
            {
                "Team": "DEN",
                "MoV": 6.7,
                "SoS": -0.3,
                "SRS": 6.4,
                "SRS_O": 0.4,
                "SRS_D": 4.3,
                "SRS_ST": 1.7,
            },
            {
                "Team": "MIN",
                "MoV": 5.9,
                "SoS": 0.4,
                "SRS": 6.3,
                "SRS_O": 1.3,
                "SRS_D": 2.5,
                "SRS_ST": 2.4,
            },
            {
                "Team": "LAC",
                "MoV": 5.9,
                "SoS": -0.6,
                "SRS": 5.3,
                "SRS_O": 0.0,
                "SRS_D": 3.0,
                "SRS_ST": 2.2,
            },
            {
                "Team": "KC",
                "MoV": 3.5,
                "SoS": 0.7,
                "SRS": 4.2,
                "SRS_O": 0.3,
                "SRS_D": 1.6,
                "SRS_ST": 2.3,
            },
            {
                "Team": "WAS",
                "MoV": 5.5,
                "SoS": -1.8,
                "SRS": 3.8,
                "SRS_O": 4.7,
                "SRS_D": -1.9,
                "SRS_ST": 1.0,
            },
            {
                "Team": "ARI",
                "MoV": 1.2,
                "SoS": 0.9,
                "SRS": 2.1,
                "SRS_O": 0.5,
                "SRS_D": 1.9,
                "SRS_ST": -0.3,
            },
            {
                "Team": "PIT",
                "MoV": 1.9,
                "SoS": 0.1,
                "SRS": 2.1,
                "SRS_O": -3.1,
                "SRS_D": 1.5,
                "SRS_ST": 3.7,
            },
            {
                "Team": "CIN",
                "MoV": 2.2,
                "SoS": -0.8,
                "SRS": 1.4,
                "SRS_O": 3.6,
                "SRS_D": -3.8,
                "SRS_ST": 1.6,
            },
            {
                "Team": "SEA",
                "MoV": 0.4,
                "SoS": 0.8,
                "SRS": 1.2,
                "SRS_O": -0.7,
                "SRS_D": 2.9,
                "SRS_ST": -0.9,
            },
            {
                "Team": "LA",
                "MoV": -1.1,
                "SoS": 1.1,
                "SRS": -0.1,
                "SRS_O": -0.3,
                "SRS_D": 0.7,
                "SRS_ST": -0.4,
            },
            {
                "Team": "HOU",
                "MoV": 0.0,
                "SoS": -0.7,
                "SRS": -0.7,
                "SRS_O": -2.4,
                "SRS_D": 0.5,
                "SRS_ST": 1.2,
            },
            {
                "Team": "SF",
                "MoV": -2.8,
                "SoS": 1.6,
                "SRS": -1.2,
                "SRS_O": 0.9,
                "SRS_D": -2.2,
                "SRS_ST": 0.2,
            },
            {
                "Team": "ATL",
                "MoV": -2.0,
                "SoS": -0.1,
                "SRS": -2.1,
                "SRS_O": -1.1,
                "SRS_D": -1.2,
                "SRS_ST": 0.2,
            },
            {
                "Team": "CHI",
                "MoV": -3.5,
                "SoS": 1.3,
                "SRS": -2.2,
                "SRS_O": -2.4,
                "SRS_D": 2.8,
                "SRS_ST": -2.7,
            },
            {
                "Team": "MIA",
                "MoV": -1.1,
                "SoS": -2.0,
                "SRS": -3.1,
                "SRS_O": -3.4,
                "SRS_D": 1.5,
                "SRS_ST": -1.1,
            },
            {
                "Team": "IND",
                "MoV": -2.9,
                "SoS": -0.8,
                "SRS": -3.7,
                "SRS_O": -0.3,
                "SRS_D": -2.5,
                "SRS_ST": -0.9,
            },
            {
                "Team": "NO",
                "MoV": -3.5,
                "SoS": -0.5,
                "SRS": -4.1,
                "SRS_O": -3.1,
                "SRS_D": 0.2,
                "SRS_ST": -1.2,
            },
            {
                "Team": "NYJ",
                "MoV": -3.9,
                "SoS": -0.6,
                "SRS": -4.5,
                "SRS_O": -0.4,
                "SRS_D": -0.7,
                "SRS_ST": -3.4,
            },
            {
                "Team": "DAL",
                "MoV": -6.9,
                "SoS": 0.6,
                "SRS": -6.3,
                "SRS_O": -5.2,
                "SRS_D": -3.4,
                "SRS_ST": 2.3,
            },
            {
                "Team": "LV",
                "MoV": -7.4,
                "SoS": 1.0,
                "SRS": -6.4,
                "SRS_O": -4.6,
                "SRS_D": -0.7,
                "SRS_ST": -1.1,
            },
            {
                "Team": "JAX",
                "MoV": -6.8,
                "SoS": -0.8,
                "SRS": -7.6,
                "SRS_O": -2.4,
                "SRS_D": -2.9,
                "SRS_ST": -2.2,
            },
            {
                "Team": "NYG",
                "MoV": -8.4,
                "SoS": 0.3,
                "SRS": -8.1,
                "SRS_O": -6.9,
                "SRS_D": 0.1,
                "SRS_ST": -1.4,
            },
            {
                "Team": "NE",
                "MoV": -7.5,
                "SoS": -0.8,
                "SRS": -8.3,
                "SRS_O": -4.3,
                "SRS_D": -1.2,
                "SRS_ST": -2.8,
            },
            {
                "Team": "TEN",
                "MoV": -8.8,
                "SoS": 0.4,
                "SRS": -8.4,
                "SRS_O": -4.2,
                "SRS_D": -1.9,
                "SRS_ST": -2.3,
            },
            {
                "Team": "CLE",
                "MoV": -10.4,
                "SoS": 1.2,
                "SRS": -9.2,
                "SRS_O": -5.1,
                "SRS_D": -2.2,
                "SRS_ST": -1.9,
            },
            {
                "Team": "CAR",
                "MoV": -11.4,
                "SoS": 0.5,
                "SRS": -10.9,
                "SRS_O": 0.0,
                "SRS_D": -7.2,
                "SRS_ST": -3.7,
            },
        ]
    )

    assert srs_frame.equals(exepcted_srs)


def test_srs_predictor():
    # Get the SRS breakdown for the end of the 2024 season
    fitter = srs_model._SrsFitter(NflWeek(2023, 1), NflWeek(2023, 18))
    fitter.fit()
    predictor = srs_model._SrsPredictor(fitter)

    # Create a sample DataFrame to predict SRS
    games = pd.DataFrame(
        [
            {
                "game_id": "2023_01_DET_KC",
                "home_team": "KC",
                "away_team": "DET",
                "is_neutral": False,
            },
            {
                "game_id": "2023_01_CAR_ATL",
                "home_team": "ATL",
                "away_team": "CAR",
                "is_neutral": False,
            },
            {
                "game_id": "2023_01_HOU_BAL",
                "home_team": "BAL",
                "away_team": "HOU",
                "is_neutral": False,
            },
            {
                "game_id": "2023_01_CIN_CLE",
                "home_team": "CLE",
                "away_team": "CIN",
                "is_neutral": False,
            },
            {
                "game_id": "2023_01_JAX_IND",
                "home_team": "IND",
                "away_team": "JAX",
                "is_neutral": False,
            },
        ]
    )

    # Predict SRS values
    predicted_games = predictor.predict(games)

    # The expected games result
    expected_games = pd.DataFrame(
        [
            {
                "game_id": "2023_01_DET_KC",
                "home_team": "KC",
                "away_team": "DET",
                "pred_spread": 2.3860685731694486,
                "pred_spread_O": -6.343678437805178,
                "pred_spread_D": 5.1536307129700125,
                "pred_spread_ST": 3.576116298004613,
            },
            {
                "game_id": "2023_01_CAR_ATL",
                "home_team": "ATL",
                "away_team": "CAR",
                "pred_spread": 7.4724593303074265,
                "pred_spread_O": 6.903121586208166,
                "pred_spread_D": 0.9321619763194577,
                "pred_spread_ST": -0.3628242322201971,
            },
            {
                "game_id": "2023_01_HOU_BAL",
                "home_team": "BAL",
                "away_team": "HOU",
                "pred_spread": 15.302268090183997,
                "pred_spread_O": 7.522905221744963,
                "pred_spread_D": 6.454350450500083,
                "pred_spread_ST": 1.3250124179389524,
            },
            {
                "game_id": "2023_01_CIN_CLE",
                "home_team": "CLE",
                "away_team": "CIN",
                "pred_spread": 4.315206827677684,
                "pred_spread_O": 0.9668275753820668,
                "pred_spread_D": 0.754832064891678,
                "pred_spread_ST": 2.593547187403938,
            },
            {
                "game_id": "2023_01_JAX_IND",
                "home_team": "IND",
                "away_team": "JAX",
                "pred_spread": -0.21316520048219978,
                "pred_spread_O": 1.265277909160397,
                "pred_spread_D": -0.5190956218394549,
                "pred_spread_ST": -0.959347487803142,
            },
        ]
    )

    # Check if the predicted games match the expected games
    assert predicted_games.equals(expected_games)
