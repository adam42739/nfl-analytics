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


def test_home_field_advantage():
    hfa, hfa_o, hfa_d, hfa_st = advanced_data.home_field_advantage(NflWeek(2024, 1), NflWeek(2024, 18))

    assert hfa == 1.7191011235955065
    assert hfa_o == 1.295880149812735
    assert hfa_d == 0.0449438202247191
    assert hfa_st == 0.37827715355805225


def test_simple_rating_system():
    # Get the SRS breakdown for the end of the 2024 season
    srs_frame = (
        advanced_data.simple_rating_system(NflWeek(2024, 1), NflWeek(2024, 18))
        .sort_values(by="SRS", ascending=False)
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
