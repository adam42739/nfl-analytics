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
