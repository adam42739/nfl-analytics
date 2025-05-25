"""
# Sourcing Module

This module provides functions to retrieve and manage NFL data from NFL Verse.
It supports fetching datasets such as play-by-play, rosters, injuries, and more,
with options for caching and local storage.
"""

import pandas as pd
from nfl_analytics import _local_storage
from typing import Literal, Callable


# all nfl data files will be stored in `[path to datastore]/nfl_data/`
_DATASTORE_SUBDIR = "nfl_data/"


def _source_web_file(
    url: str, file_type: Literal["csv", "parquet", "csv.gz"]
) -> pd.DataFrame:
    """
    Source a file from the given URL.

    Parameters
    ----------
    url : str
        The URL of the file to load.
    file_type : {"csv", "parquet", "csv.gz"}
        The type of file to load.
    """
    if file_type == "csv":
        return pd.read_csv(url)
    elif file_type == "parquet":
        return pd.read_parquet(url)
    elif file_type == "csv.gz":
        return pd.read_csv(url, compression="gzip")


_PLAYERS_URL = "https://github.com/nflverse/nflverse-data/releases/download/players/players.parquet"
_PBP_URL = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{year}.parquet"
_SCHEDULES_URL = "http://www.habitatring.com/games.csv"
_PARTICIPATION_URL = "https://github.com/nflverse/nflverse-data/releases/download/pbp_participation/pbp_participation_{year}.parquet"
_WEEKLY_STATS_URL = "https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats.parquet"
_ROSTER_URL = "https://github.com/nflverse/nflverse-data/releases/download/{freq_name}_{year}.parquet"
_TEAM_DESC_URL = (
    "https://github.com/nflverse/nflfastR-data/raw/master/teams_colors_logos.csv"
)
_OFFICIALS_URL = (
    "https://raw.githubusercontent.com/nflverse/nfldata/master/data/officials.csv"
)
_SCORE_LINES_URL = (
    "https://raw.githubusercontent.com/nflverse/nfldata/master/data/sc_lines.csv"
)
_DRAFT_PICKS_URL = "https://github.com/nflverse/nflverse-data/releases/download/draft_picks/draft_picks.parquet"
_COMBINE_URL = "https://github.com/nflverse/nflverse-data/releases/download/combine/combine.parquet"
_ID_MAP_URL = "https://raw.githubusercontent.com/dynastyprocess/data/master/files/db_playerids.csv"
_NGS_URL = "https://github.com/nflverse/nflverse-data/releases/download/nextgen_stats/ngs_{year}_{ngs_type}.csv.gz"
_DEPTH_CHART_URL = "https://github.com/nflverse/nflverse-data/releases/download/depth_charts/depth_charts_{year}.parquet"
_INJURIES_URL = "https://github.com/nflverse/nflverse-data/releases/download/injuries/injuries_{year}.parquet"
_QBR_URL = "https://raw.githubusercontent.com/nflverse/espnscrapeR-data/master/data/qbr-{level}-{freq}.csv"
_PFR_SEASON_URL = "https://github.com/nflverse/nflverse-data/releases/download/pfr_advstats/advstats_season_{s_type}.parquet"
_PFR_WEEK_URL = "https://github.com/nflverse/nflverse-data/releases/download/pfr_advstats/advstats_week_{s_type}_{year}.parquet"
_SNAP_COUNT_URL = "https://github.com/nflverse/nflverse-data/releases/download/snap_counts/snap_counts_{year}.parquet"
_FTN_URL = "https://github.com/nflverse/nflverse-data/releases/download/ftn_charting/ftn_charting_{year}.parquet"


# This is a helper dict for the `_ROSTER_URL` to get the correct url for each frequency
_ROSTER_FREQ_NAME = {
    "weekly": "weekly_rosters/roster_weekly",
    "season": "rosters/roster",
}


# All the functions to source data from NFL Verse
_SOURCE_FUNCTIONS: dict[str, Callable[[dict], pd.DataFrame]] = {
    "players": lambda _: _source_web_file(_PLAYERS_URL, "parquet"),
    "pbp": lambda args: _source_web_file(
        _PBP_URL.format(year=str(args["year"])), "parquet"
    ),
    "schedules": lambda _: _source_web_file(_SCHEDULES_URL, "csv"),
    "participation": lambda args: _source_web_file(
        _PARTICIPATION_URL.format(year=str(args["year"])), "parquet"
    ),
    "weekly_stats": lambda _: _source_web_file(_WEEKLY_STATS_URL, "parquet"),
    "rosters": lambda args: _source_web_file(
        _ROSTER_URL.format(
            year=str(args["year"]),
            freq_name=_ROSTER_FREQ_NAME[args["freq"]],
        ),
        "parquet",
    ),
    "team_desc": lambda _: _source_web_file(_TEAM_DESC_URL, "csv"),
    "officials": lambda _: _source_web_file(_OFFICIALS_URL, "csv"),
    "score_lines": lambda _: _source_web_file(_SCORE_LINES_URL, "csv"),
    "draft_picks": lambda _: _source_web_file(_DRAFT_PICKS_URL, "parquet"),
    "combine": lambda _: _source_web_file(_COMBINE_URL, "parquet"),
    "id_map": lambda _: _source_web_file(_ID_MAP_URL, "csv"),
    "ngs": lambda args: _source_web_file(
        _NGS_URL.format(year=str(args["year"]), ngs_type=args["ngs_type"]), "csv.gz"
    ),
    "depth_chart": lambda args: _source_web_file(
        _DEPTH_CHART_URL.format(year=str(args["year"])), "parquet"
    ),
    "injuries": lambda args: _source_web_file(
        _INJURIES_URL.format(year=str(args["year"])), "parquet"
    ),
    "qbr": lambda args: _source_web_file(
        _QBR_URL.format(level=args["level"], freq=args["freq"]), "csv"
    ),
    "pfr_season": lambda args: _source_web_file(
        _PFR_SEASON_URL.format(s_type=args["s_type"]),
        "parquet",
    ),
    "pfr_week": lambda args: _source_web_file(
        _PFR_WEEK_URL.format(s_type=args["s_type"], year=str(args["year"])), "parquet"
    ),
    "snap_counts": lambda args: _source_web_file(
        _SNAP_COUNT_URL.format(year=str(args["year"])), "parquet"
    ),
    "ftn": lambda args: _source_web_file(
        _FTN_URL.format(year=str(args["year"])), "parquet"
    ),
}


def get(
    data_type: Literal[
        "players",
        "pbp",
        "schedules",
        "participation",
        "weekly_stats",
        "rosters",
        "team_desc",
        "officials",
        "score_lines",
        "draft_picks",
        "combine",
        "id_map",
        "ngs",
        "depth_chart",
        "injuries",
        "qbr",
        "pfr_season",
        "pfr_week",
        "snap_counts",
        "ftn",
    ],
    force_refresh: bool = False,
    args: dict = None,
) -> pd.DataFrame:
    """
    Get the specific data from the web or from the local storage.

    Parameters
    ----------
    data_type : {"players", "pbp", "schedules", "participation", "weekly_stats", "rosters", "team_desc", "officials", "score_lines", "draft_picks", "combine", "id_map", "ngs", "depth_chart", "injuries", "qbr", "pfr_season", "pfr_week", "snap_counts", "ftn"}
        The type of data to get.
    force_refresh : bool
        If True, we automatically get the most up-to-date data from NFL Verse and overwrite the local file.
    args : dict
        The arguments to pass to the source function.
    """
    # the file name to save the data to
    filename = f"{data_type}.parquet"
    if args:
        args_str = "-".join([f"{k}={v}" for k, v in sorted(args.items())])
        filename = f"{data_type}-{args_str}.parquet"

    # if we are not forcing a refresh and the file exists, load the file, otherwise imprort from NFL Verse
    if not force_refresh and _local_storage.file_exists(_DATASTORE_SUBDIR, filename):
        # load the file
        df = _local_storage.load_frame(_DATASTORE_SUBDIR, filename)

        return df
    else:
        # get the data from the API
        df = _SOURCE_FUNCTIONS[data_type](args)

        # dump the file
        _local_storage.dump_frame(df, _DATASTORE_SUBDIR, filename)

        return df
