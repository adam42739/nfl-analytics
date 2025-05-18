import tempfile
from nfl_analytics import _local_storage
from typing import Callable
import pandas as pd
from nfl_analytics.nfl_data import sourcing


def run_data_fetch_test(
    data_fetcher: Callable[[], pd.DataFrame],
    expected_columns: list[str],
    file_path: str,
    **fetcher_args
):
    """
    Helper function to test data fetching functions.

    Parameters
    ----------
    data_fetcher : Callable
        The function to fetch data (e.g., nfl_data.get_players).
    expected_columns : list
        The list of expected columns in the resulting DataFrame.
    file_path : str
        The expected file path in the datastore.
    fetcher_args : dict
        Additional arguments to pass to the data_fetcher function.
    """
    with tempfile.TemporaryDirectory() as tempdir:
        # Get the current datastore path
        current_path = _local_storage._get_datastore_path()

        try:
            # Set the datastore path to a temporary directory
            _local_storage.set_datastore_path(tempdir)

            # Fetch the data
            df = data_fetcher(**fetcher_args)

            # Check that the DataFrame has the expected columns
            for col in expected_columns:
                assert col in df.columns

            # Check that the file exists in the datastore
            assert _local_storage.file_exists("nfl_data/", file_path)
        finally:
            # Reset the datastore path to the original path
            _local_storage.set_datastore_path(current_path)


def test_get_players():
    run_data_fetch_test(
        data_fetcher=sourcing.get_players,
        expected_columns=[
            "college_conference",
            "current_team_id",
            "display_name",
            "draft_club",
        ],
        file_path="players.parquet",
    )


def test_get_pbp():
    run_data_fetch_test(
        data_fetcher=sourcing.get_pbp,
        expected_columns=[
            "play_id",
            "game_id",
            "old_game_id",
            "home_team",
            "away_team",
        ],
        file_path="pbp-year=2023.parquet",
        year=2023,
    )


def test_get_schedules():
    run_data_fetch_test(
        data_fetcher=sourcing.get_schedules,
        expected_columns=[
            "game_id",
            "season",
            "game_type",
            "week",
            "gameday",
            "weekday",
        ],
        file_path="schedules.parquet",
    )


def test_get_participation():
    run_data_fetch_test(
        data_fetcher=sourcing.get_participation,
        expected_columns=[
            "nflverse_game_id",
            "old_game_id",
            "play_id",
            "possession_team",
            "offense_formation",
            "offense_personnel",
        ],
        file_path="participation-year=2023.parquet",
        year=2023,
    )


def test_get_weekly_stats():
    run_data_fetch_test(
        data_fetcher=sourcing.get_weekly_stats,
        expected_columns=[
            "player_id",
            "player_name",
            "player_display_name",
            "position",
        ],
        file_path="weekly_stats.parquet",
    )


def test_get_roster():
    run_data_fetch_test(
        data_fetcher=sourcing.get_roster,
        expected_columns=[
            "season",
            "team",
            "position",
            "depth_chart_position",
            "jersey_number",
        ],
        file_path="rosters-freq=weekly-year=2023.parquet",
        year=2023,
        freq="weekly",
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_roster,
        expected_columns=[
            "season",
            "team",
            "position",
            "depth_chart_position",
            "jersey_number",
        ],
        file_path="rosters-freq=season-year=2023.parquet",
        year=2023,
        freq="season",
    )


def test_get_team_desc():
    run_data_fetch_test(
        data_fetcher=sourcing.get_team_desc,
        expected_columns=[
            "team_division",
            "team_color",
            "team_color2",
            "team_color3",
        ],
        file_path="team_desc.parquet",
    )


def test_get_officials():
    run_data_fetch_test(
        data_fetcher=sourcing.get_officials,
        expected_columns=[
            "game_id",
            "off_pos",
            "official_id",
            "name",
        ],
        file_path="officials.parquet",
    )


def test_get_score_lines():
    run_data_fetch_test(
        data_fetcher=sourcing.get_score_lines,
        expected_columns=[
            "away_team",
            "home_team",
            "game_id",
            "side",
            "line",
        ],
        file_path="score_lines.parquet",
    )


def test_get_draft_picks():
    run_data_fetch_test(
        data_fetcher=sourcing.get_draft_picks,
        expected_columns=[
            "cfb_player_id",
            "pfr_player_name",
            "hof",
            "position",
            "category",
        ],
        file_path="draft_picks.parquet",
    )


def test_get_combine():
    run_data_fetch_test(
        data_fetcher=sourcing.get_combine,
        expected_columns=[
            "pfr_id",
            "cfb_id",
            "player_name",
            "pos",
            "school",
            "ht",
            "wt",
            "forty",
        ],
        file_path="combine.parquet",
    )


def test_get_id_map():
    run_data_fetch_test(
        data_fetcher=sourcing.get_id_map,
        expected_columns=[
            "sleeper_id",
            "nfl_id",
            "espn_id",
            "yahoo_id",
            "fleaflicker_id",
        ],
        file_path="id_map.parquet",
    )


def test_get_ngs():
    run_data_fetch_test(
        data_fetcher=sourcing.get_ngs,
        expected_columns=[
            "percent_attempts_gte_eight_defenders",
            "avg_time_to_los",
            "rush_attempts",
            "rush_yards",
            "expected_rush_yards",
        ],
        file_path="ngs-ngs_type=rushing-year=2023.parquet",
        year=2023,
        ngs_type="rushing",
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_ngs,
        expected_columns=[
            "avg_completed_air_yards",
            "avg_intended_air_yards",
            "avg_air_yards_differential",
            "aggressiveness",
            "max_completed_air_distance",
            "avg_air_yards_to_sticks",
            "attempts",
        ],
        file_path="ngs-ngs_type=passing-year=2023.parquet",
        year=2023,
        ngs_type="passing",
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_ngs,
        expected_columns=[
            "avg_intended_air_yards",
            "percent_share_of_intended_air_yards",
            "receptions",
            "targets",
            "catch_percentage",
            "yards",
            "rec_touchdowns",
            "avg_yac",
            "avg_expected_yac",
            "avg_yac_above_expectation",
        ],
        file_path="ngs-ngs_type=receiving-year=2023.parquet",
        year=2023,
        ngs_type="receiving",
    )


def test_get_depth_chart():
    run_data_fetch_test(
        data_fetcher=sourcing.get_depth_chart,
        expected_columns=[
            "season",
            "club_code",
            "week",
            "game_type",
            "depth_team",
            "last_name",
            "first_name",
            "football_name",
            "formation",
            "gsis_id",
            "jersey_number",
        ],
        file_path="depth_chart-year=2023.parquet",
        year=2023,
    )


def test_get_injuries():
    run_data_fetch_test(
        data_fetcher=sourcing.get_injuries,
        expected_columns=[
            "report_secondary_injury",
            "report_status",
            "practice_primary_injury",
            "practice_secondary_injury",
            "practice_status",
            "date_modified",
        ],
        file_path="injuries-year=2023.parquet",
        year=2023,
    )


def test_get_qbr():
    run_data_fetch_test(
        data_fetcher=sourcing.get_qbr,
        expected_columns=[
            "name_first",
            "name_last",
            "name_display",
            "name_short",
            "age",
            "team_name",
            "team_short_name",
            "slug",
            "team_id",
            "team_uid",
        ],
        file_path="qbr-freq=season-level=college.parquet",
        level="college",
        freq="season",
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_qbr,
        expected_columns=[
            "qbr_total",
            "pts_added",
            "qb_plays",
            "epa_total",
            "pass",
            "run",
            "exp_sack",
            "penalty",
            "qbr_raw",
            "sack",
            "headshot_href",
            "flag",
        ],
        file_path="qbr-freq=weekly-level=college.parquet",
        level="college",
        freq="weekly",
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_qbr,
        expected_columns=[
            "pass",
            "run",
            "exp_sack",
            "penalty",
            "qbr_raw",
            "sack",
            "name_first",
            "name_last",
            "name_display",
            "headshot_href",
            "team",
            "qualified",
        ],
        file_path="qbr-freq=season-level=nfl.parquet",
        level="nfl",
        freq="season",
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_qbr,
        expected_columns=[
            "qb_plays",
            "epa_total",
            "pass",
            "run",
            "exp_sack",
            "penalty",
            "qbr_raw",
            "sack",
            "name_first",
            "name_last",
            "name_display",
        ],
        file_path="qbr-freq=weekly-level=nfl.parquet",
        level="nfl",
        freq="weekly",
    )


def test_get_pfr():
    run_data_fetch_test(
        data_fetcher=sourcing.get_pfr,
        expected_columns=[
            "season",
            "player",
            "pfr_id",
            "tm",
            "age",
            "pos",
            "g",
            "gs",
            "int",
            "tgt",
        ],
        file_path="pfr_season-s_type=def.parquet",
        s_type="def",
        freq="season",
        year=2023,
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_pfr,
        expected_columns=[
            "pocket_time",
            "times_blitzed",
            "times_hurried",
            "times_hit",
            "times_pressured",
            "pressure_pct",
            "batted_balls",
            "on_tgt_throws",
            "on_tgt_pct",
            "rpo_plays",
            "rpo_yards",
            "rpo_pass_att",
        ],
        file_path="pfr_season-s_type=pass.parquet",
        s_type="pass",
        freq="season",
        year=2023,
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_pfr,
        expected_columns=[
            "yds",
            "td",
            "x1d",
            "ybc",
            "ybc_att",
            "yac",
            "yac_att",
            "brk_tkl",
            "att_br",
            "loaded",
        ],
        file_path="pfr_season-s_type=rush.parquet",
        s_type="rush",
        freq="season",
        year=2023,
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_pfr,
        expected_columns=[
            "season",
            "player",
            "pfr_id",
            "tm",
            "age",
            "pos",
            "g",
            "gs",
            "tgt",
            "rec",
            "yds",
            "td",
            "x1d",
            "ybc",
            "ybc_r",
            "yac",
            "yac_r",
            "adot",
        ],
        file_path="pfr_season-s_type=rec.parquet",
        s_type="rec",
        freq="season",
        year=2023,
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_pfr,
        expected_columns=[
            "def_targets",
            "def_completions_allowed",
            "def_completion_pct",
            "def_yards_allowed",
            "def_yards_allowed_per_cmp",
            "def_yards_allowed_per_tgt",
            "def_receiving_td_allowed",
            "def_passer_rating_allowed",
            "def_adot",
            "def_air_yards_completed",
        ],
        file_path="pfr_week-s_type=def-year=2023.parquet",
        s_type="def",
        freq="week",
        year=2023,
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_pfr,
        expected_columns=[
            "opponent",
            "pfr_player_name",
            "pfr_player_id",
            "passing_drops",
            "passing_drop_pct",
            "receiving_drop",
            "receiving_drop_pct",
            "passing_bad_throws",
            "passing_bad_throw_pct",
            "times_sacked",
        ],
        file_path="pfr_week-s_type=pass-year=2023.parquet",
        s_type="pass",
        freq="week",
        year=2023,
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_pfr,
        expected_columns=[
            "opponent",
            "pfr_player_name",
            "pfr_player_id",
            "carries",
            "rushing_yards_before_contact",
            "rushing_yards_before_contact_avg",
            "rushing_yards_after_contact",
            "rushing_yards_after_contact_avg",
        ],
        file_path="pfr_week-s_type=rush-year=2023.parquet",
        s_type="rush",
        freq="week",
        year=2023,
    )
    run_data_fetch_test(
        data_fetcher=sourcing.get_pfr,
        expected_columns=[
            "opponent",
            "pfr_player_name",
            "pfr_player_id",
            "rushing_broken_tackles",
            "receiving_broken_tackles",
            "passing_drops",
            "passing_drop_pct",
            "receiving_drop",
            "receiving_drop_pct",
        ],
        file_path="pfr_week-s_type=rec-year=2023.parquet",
        s_type="rec",
        freq="week",
        year=2023,
    )


def test_get_snap_counts():
    run_data_fetch_test(
        data_fetcher=sourcing.get_snap_counts,
        expected_columns=[
            "pfr_player_id",
            "position",
            "team",
            "opponent",
            "offense_snaps",
            "offense_pct",
            "defense_snaps",
            "defense_pct",
            "st_snaps",
            "st_pct",
        ],
        file_path="snap_counts-year=2023.parquet",
        year=2023,
    )


def test_get_ftn():
    run_data_fetch_test(
        data_fetcher=sourcing.get_ftn,
        expected_columns=[
            "n_offense_backfield",
            "n_defense_box",
            "is_no_huddle",
            "is_motion",
            "is_play_action",
            "is_screen_pass",
            "is_rpo",
            "is_trick_play",
            "is_qb_out_of_pocket",
            "is_interception_worthy",
            "is_throw_away",
        ],
        file_path="ftn-year=2023.parquet",
        year=2023,
    )
