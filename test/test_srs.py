from nfl_analytics import srs
import pandas as pd


def test_get_srs():
    # Get the SRS for the end of the 2024 season
    srs2024 = srs.get_srs(2024, 18)
    srs2024 = (
        srs2024.sort_values(by="SRS", ascending=False).round(1).reset_index(drop=True)
    )

    # The expected SRS results
    expected_SRS = pd.DataFrame(
        [
            {"Team": "DET", "SRS": 13.8},
            {"Team": "BAL", "SRS": 9.9},
            {"Team": "GB", "SRS": 8.1},
            {"Team": "BUF", "SRS": 8.1},
            {"Team": "PHI", "SRS": 7.7},
            {"Team": "TB", "SRS": 6.4},
            {"Team": "DEN", "SRS": 6.4},
            {"Team": "MIN", "SRS": 6.2},
            {"Team": "LAC", "SRS": 5.3},
            {"Team": "KC", "SRS": 4.2},
            {"Team": "WAS", "SRS": 3.7},
            {"Team": "ARI", "SRS": 2.1},
            {"Team": "PIT", "SRS": 2.1},
            {"Team": "CIN", "SRS": 1.4},
            {"Team": "SEA", "SRS": 1.3},
            {"Team": "LA", "SRS": -0.1},
            {"Team": "HOU", "SRS": -0.7},
            {"Team": "SF", "SRS": -1.2},
            {"Team": "ATL", "SRS": -2.2},
            {"Team": "CHI", "SRS": -2.3},
            {"Team": "MIA", "SRS": -3.0},
            {"Team": "IND", "SRS": -3.7},
            {"Team": "NO", "SRS": -4.1},
            {"Team": "NYJ", "SRS": -4.3},
            {"Team": "DAL", "SRS": -6.3},
            {"Team": "LV", "SRS": -6.4},
            {"Team": "JAX", "SRS": -7.5},
            {"Team": "NYG", "SRS": -8.0},
            {"Team": "NE", "SRS": -8.1},
            {"Team": "TEN", "SRS": -8.4},
            {"Team": "CLE", "SRS": -9.2},
            {"Team": "CAR", "SRS": -11.0},
        ]
    )

    assert srs2024.equals(expected_SRS)


def test_get_srs_breakdown():
    # Get the SRS breakdown for the end of the 2024 season
    srs2024 = srs.get_srs_breakdown(2024, 18)
    srs2024 = (
        srs2024.sort_values(by="SRS", ascending=False).round(1).reset_index(drop=True)
    )

    # The expected SRS results
    expected_SRS = pd.DataFrame(
        [
            {"Team": "DET", "SRS_O": 9.8, "SRS_D": 2.1, "SRS_ST": 1.9, "SRS": 13.8},
            {"Team": "BAL", "SRS_O": 7.8, "SRS_D": 0.6, "SRS_ST": 1.5, "SRS": 9.9},
            {"Team": "GB", "SRS_O": 4.3, "SRS_D": 2.0, "SRS_ST": 1.8, "SRS": 8.1},
            {"Team": "BUF", "SRS_O": 7.8, "SRS_D": 0.0, "SRS_ST": 0.3, "SRS": 8.1},
            {"Team": "PHI", "SRS_O": 3.1, "SRS_D": 2.6, "SRS_ST": 1.9, "SRS": 7.7},
            {"Team": "TB", "SRS_O": 5.3, "SRS_D": 0.7, "SRS_ST": 0.4, "SRS": 6.4},
            {"Team": "DEN", "SRS_O": 0.4, "SRS_D": 4.3, "SRS_ST": 1.7, "SRS": 6.4},
            {"Team": "MIN", "SRS_O": 1.3, "SRS_D": 2.5, "SRS_ST": 2.4, "SRS": 6.2},
            {"Team": "LAC", "SRS_O": 0.0, "SRS_D": 3.0, "SRS_ST": 2.2, "SRS": 5.3},
            {"Team": "KC", "SRS_O": 0.3, "SRS_D": 1.6, "SRS_ST": 2.3, "SRS": 4.2},
            {"Team": "WAS", "SRS_O": 4.7, "SRS_D": -1.9, "SRS_ST": 1.0, "SRS": 3.7},
            {"Team": "ARI", "SRS_O": 0.5, "SRS_D": 1.9, "SRS_ST": -0.3, "SRS": 2.1},
            {"Team": "PIT", "SRS_O": -3.1, "SRS_D": 1.5, "SRS_ST": 3.7, "SRS": 2.1},
            {"Team": "CIN", "SRS_O": 3.6, "SRS_D": -3.8, "SRS_ST": 1.6, "SRS": 1.4},
            {"Team": "SEA", "SRS_O": -0.7, "SRS_D": 2.9, "SRS_ST": -0.9, "SRS": 1.3},
            {"Team": "LA", "SRS_O": -0.3, "SRS_D": 0.7, "SRS_ST": -0.4, "SRS": -0.1},
            {"Team": "HOU", "SRS_O": -2.4, "SRS_D": 0.5, "SRS_ST": 1.2, "SRS": -0.7},
            {"Team": "SF", "SRS_O": 0.9, "SRS_D": -2.2, "SRS_ST": 0.2, "SRS": -1.2},
            {"Team": "ATL", "SRS_O": -1.1, "SRS_D": -1.2, "SRS_ST": 0.2, "SRS": -2.2},
            {"Team": "CHI", "SRS_O": -2.4, "SRS_D": 2.8, "SRS_ST": -2.7, "SRS": -2.3},
            {"Team": "MIA", "SRS_O": -3.4, "SRS_D": 1.5, "SRS_ST": -1.1, "SRS": -3.0},
            {"Team": "IND", "SRS_O": -0.3, "SRS_D": -2.5, "SRS_ST": -0.9, "SRS": -3.7},
            {"Team": "NO", "SRS_O": -3.1, "SRS_D": 0.2, "SRS_ST": -1.2, "SRS": -4.1},
            {"Team": "NYJ", "SRS_O": -0.4, "SRS_D": -0.6, "SRS_ST": -3.3, "SRS": -4.3},
            {"Team": "DAL", "SRS_O": -5.2, "SRS_D": -3.4, "SRS_ST": 2.3, "SRS": -6.3},
            {"Team": "LV", "SRS_O": -4.6, "SRS_D": -0.7, "SRS_ST": -1.1, "SRS": -6.4},
            {"Team": "JAX", "SRS_O": -2.5, "SRS_D": -2.8, "SRS_ST": -2.2, "SRS": -7.5},
            {"Team": "NYG", "SRS_O": -6.9, "SRS_D": 0.2, "SRS_ST": -1.4, "SRS": -8.0},
            {"Team": "NE", "SRS_O": -4.3, "SRS_D": -1.1, "SRS_ST": -2.7, "SRS": -8.1},
            {"Team": "TEN", "SRS_O": -4.2, "SRS_D": -1.9, "SRS_ST": -2.3, "SRS": -8.4},
            {"Team": "CLE", "SRS_O": -5.1, "SRS_D": -2.2, "SRS_ST": -1.9, "SRS": -9.2},
            {"Team": "CAR", "SRS_O": -0.1, "SRS_D": -7.2, "SRS_ST": -3.7, "SRS": -11.0},
        ]
    )

    assert srs2024.equals(expected_SRS)
