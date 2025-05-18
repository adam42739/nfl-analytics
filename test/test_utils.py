from nfl_analytics import utils
import pandas as pd


def test_filter_data():
    # Create a sample DataFrame
    data = {
        "season": [2022, 2023, 2023, 2024],
        "week": [1, 2, 3, 1],
        "team": ["Team A", "Team B", "Team C", "Team D"],
    }
    df = pd.DataFrame(data)

    # Define the start and end weeks
    start_week = utils.NflWeek(2023, 2)
    end_week = utils.NflWeek(2023, 3)

    # Filter the DataFrame: start_week to end_week
    filtered_df = utils.filter_data(
        df, start_week=start_week, end_week=end_week
    ).reset_index(drop=True)

    # Check the result
    expected_data = {
        "season": [2023, 2023],
        "week": [2, 3],
        "team": ["Team B", "Team C"],
    }
    expected_df = pd.DataFrame(expected_data)

    assert filtered_df.equals(expected_df)

    # Filter the DataFrame: up to end_week
    filtered_df = utils.filter_data(df, end_week=end_week).reset_index(drop=True)

    # Check the result
    expected_data = {
        "season": [2022, 2023, 2023],
        "week": [1, 2, 3],
        "team": ["Team A", "Team B", "Team C"],
    }
    expected_df = pd.DataFrame(expected_data)

    assert filtered_df.equals(expected_df)

    # Filter the DataFrame: start_week onwards
    filtered_df = utils.filter_data(df, start_week=start_week).reset_index(drop=True)

    # Check the result
    expected_data = {
        "season": [2023, 2023, 2024],
        "week": [2, 3, 1],
        "team": ["Team B", "Team C", "Team D"],
    }
    expected_df = pd.DataFrame(expected_data)

    assert filtered_df.equals(expected_df)


def test_point_breakdown():
    # Calculate the point breakdown
    point_breakdown = utils.point_breakdown(2024).reset_index()

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
