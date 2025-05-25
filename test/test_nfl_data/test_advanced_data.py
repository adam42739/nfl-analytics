from nfl_analytics.nfl_data import advanced_data
from nfl_analytics.nfl_data import NflWeek
import pandas as pd


def test_get_point_breakdown():
    # Calculate the point breakdown
    point_breakdown = advanced_data.point_breakdown(
        NflWeek(2024, 1), NflWeek(2024, 1)
    ).reset_index()

    # THe expected result
    expected_df = pd.DataFrame(
        [
            {
                "game_id": "2024_01_ARI_BUF",
                "home_team": "BUF",
                "away_team": "ARI",
                "home_offensive_points": 24.0,
                "away_offensive_points": 14.0,
                "home_defensive_points": 0.0,
                "away_defensive_points": 0.0,
                "home_special_teams_points": 10.0,
                "away_special_teams_points": 14.0,
            },
            {
                "game_id": "2024_01_BAL_KC",
                "home_team": "KC",
                "away_team": "BAL",
                "home_offensive_points": 18.0,
                "away_offensive_points": 12.0,
                "home_defensive_points": 0.0,
                "away_defensive_points": 0.0,
                "home_special_teams_points": 9.0,
                "away_special_teams_points": 8.0,
            },
            {
                "game_id": "2024_01_CAR_NO",
                "home_team": "NO",
                "away_team": "CAR",
                "home_offensive_points": 30.0,
                "away_offensive_points": 6.0,
                "home_defensive_points": 0.0,
                "away_defensive_points": 0.0,
                "home_special_teams_points": 17.0,
                "away_special_teams_points": 4.0,
            },
            {
                "game_id": "2024_01_DAL_CLE",
                "home_team": "CLE",
                "away_team": "DAL",
                "home_offensive_points": 12.0,
                "away_offensive_points": 12.0,
                "home_defensive_points": 0.0,
                "away_defensive_points": 0.0,
                "home_special_teams_points": 5.0,
                "away_special_teams_points": 21.0,
            },
            {
                "game_id": "2024_01_DEN_SEA",
                "home_team": "SEA",
                "away_team": "DEN",
                "home_offensive_points": 18.0,
                "away_offensive_points": 6.0,
                "home_defensive_points": 0.0,
                "away_defensive_points": 4.0,
                "home_special_teams_points": 8.0,
                "away_special_teams_points": 10.0,
            },
            {
                "game_id": "2024_01_GB_PHI",
                "home_team": "PHI",
                "away_team": "GB",
                "home_offensive_points": 24.0,
                "away_offensive_points": 18.0,
                "home_defensive_points": 0.0,
                "away_defensive_points": 0.0,
                "home_special_teams_points": 10.0,
                "away_special_teams_points": 11.0,
            },
            {
                "game_id": "2024_01_HOU_IND",
                "home_team": "IND",
                "away_team": "HOU",
                "home_offensive_points": 24.0,
                "away_offensive_points": 18.0,
                "home_defensive_points": 0.0,
                "away_defensive_points": 0.0,
                "home_special_teams_points": 3.0,
                "away_special_teams_points": 11.0,
            },
            {
                "game_id": "2024_01_JAX_MIA",
                "home_team": "MIA",
                "away_team": "JAX",
                "home_offensive_points": 12.0,
                "away_offensive_points": 12.0,
                "home_defensive_points": 0.0,
                "away_defensive_points": 0.0,
                "home_special_teams_points": 8.0,
                "away_special_teams_points": 5.0,
            },
            {
                "game_id": "2024_01_LA_DET",
                "home_team": "DET",
                "away_team": "LA",
                "home_offensive_points": 18.0,
                "away_offensive_points": 12.0,
                "home_defensive_points": 0.0,
                "away_defensive_points": 0.0,
                "home_special_teams_points": 8.0,
                "away_special_teams_points": 8.0,
            },
            {
                "game_id": "2024_01_LV_LAC",
                "home_team": "LAC",
                "away_team": "LV",
                "home_offensive_points": 12.0,
                "away_offensive_points": 6.0,
                "home_defensive_points": 0.0,
                "away_defensive_points": 0.0,
                "home_special_teams_points": 10.0,
                "away_special_teams_points": 4.0,
            },
        ]
    )

    # Get the matching records
    point_breakdown = point_breakdown[
        point_breakdown["game_id"].isin(expected_df["game_id"])
    ].reset_index(drop=True)

    assert point_breakdown.equals(expected_df)


def test_get_margin_of_victory():
    # Calculate the MOV
    mov = advanced_data.margin_of_victory(NflWeek(2024, 1), NflWeek(2024, 1))

    # The expected result
    expected_df = pd.DataFrame(
        [
            {"Team": "ARI", "MoV": -6.0},
            {"Team": "ATL", "MoV": -8.0},
            {"Team": "BAL", "MoV": -7.0},
            {"Team": "BUF", "MoV": 6.0},
            {"Team": "CAR", "MoV": -37.0},
            {"Team": "CHI", "MoV": 7.0},
            {"Team": "CIN", "MoV": -6.0},
            {"Team": "CLE", "MoV": -16.0},
            {"Team": "DAL", "MoV": 16.0},
            {"Team": "DEN", "MoV": -6.0},
            {"Team": "DET", "MoV": 6.0},
            {"Team": "GB", "MoV": -5.0},
            {"Team": "HOU", "MoV": 2.0},
            {"Team": "IND", "MoV": -2.0},
            {"Team": "JAX", "MoV": -3.0},
            {"Team": "KC", "MoV": 7.0},
            {"Team": "LA", "MoV": -6.0},
            {"Team": "LAC", "MoV": 12.0},
            {"Team": "LV", "MoV": -12.0},
            {"Team": "MIA", "MoV": 3.0},
            {"Team": "MIN", "MoV": 22.0},
            {"Team": "NE", "MoV": 6.0},
            {"Team": "NO", "MoV": 37.0},
            {"Team": "NYG", "MoV": -22.0},
            {"Team": "NYJ", "MoV": -13.0},
            {"Team": "PHI", "MoV": 5.0},
            {"Team": "PIT", "MoV": 8.0},
            {"Team": "SEA", "MoV": 6.0},
            {"Team": "SF", "MoV": 13.0},
            {"Team": "TB", "MoV": 17.0},
            {"Team": "TEN", "MoV": -7.0},
            {"Team": "WAS", "MoV": -17.0},
        ]
    )

    assert mov.equals(expected_df)
