"""
# Sourcing Module

This module provides functions to retrieve and manage NFL data from the NFL Verse. 
It supports fetching datasets such as play-by-play, rosters, injuries, and more, 
with options for caching and local storage.

Functions:
- get_players: Fetch player data.
- get_pbp: Fetch play-by-play data for a specific year.
- get_schedules: Fetch game schedules.
- get_participation: Fetch play-by-play participation data.
- get_weekly_stats: Fetch weekly player statistics.
- get_roster: Fetch roster data (weekly or seasonal).
- get_team_desc: Fetch team descriptions (logos, colors, etc.).
- get_officials: Fetch officials data.
- get_score_lines: Fetch score lines data.
- get_draft_picks: Fetch draft picks data.
- get_combine: Fetch NFL combine data.
- get_id_map: Fetch player ID mapping data.
- get_ngs: Fetch Next Gen Stats data.
- get_depth_chart: Fetch depth chart data.
- get_injuries: Fetch injury data.
- get_qbr: Fetch QBR data.
- get_pfr: Fetch Pro Football Reference data.
- get_snap_counts: Fetch snap counts data.
- get_ftn: Fetch FTN charting data.

Example:
```python
from nfl_analytics import nfl_data

pbp = nfl_data.get_pbp(year=2023)
```
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
    Source a web file from the given URL.

    Parameters
    ----------
    url : str
        The URL of the file to load.
    file_type : str
        The type of file to load. Can be either "csv" or "parquet".
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


def _get_data(
    data_type: str, force_refresh: bool = False, args: dict = None
) -> pd.DataFrame:
    """
    Get the NFL Verse data.

    Parameters
    ----------
    force_refresh : bool
        If True, we automatically get the most up-to-date data from NFL Verse and overwrite the local file.
    data_type : str
        The type of data to get.
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


def get_players(force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the players data from the NFL Verse.

    Parameters
    ----------
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("players", force_refresh)


def get_pbp(year: int, force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the play-by-play data from the NFL Verse.

    Parameters
    ----------
    year : int
        The year to get the data for. Valid years are 1999 to the present.
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("pbp", force_refresh, args={"year": year})


def get_schedules(force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the schedules data from NFL Verse.

    Parameters
    ----------
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("schedules", force_refresh)


def get_participation(year: int, force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the play-by-play participation data from the NFL Verse.

    Parameters
    ----------
    year : int
        The year to get the data for. Valid years are 2016 to 2024.
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("participation", force_refresh, args={"year": year})


def get_weekly_stats(force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the weekly stats data from the NFL Verse.

    Parameters
    ----------
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("weekly_stats", force_refresh)


def get_roster(
    year: int, freq: Literal["weekly", "season"], force_refresh: bool = False
) -> pd.DataFrame:
    """
    Get the weekly roster data from the NFL Verse.

    Parameters
    ----------
    year : int
        The year to get the data for. Valid years are:
        - 2002 to the present for "weekly" frequency.
        - 1920 to the present for "season" frequency.
    freq : str
        The frequency of the roster data ("weekly" or "season").
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("rosters", force_refresh, args={"year": year, "freq": freq})


def get_team_desc(force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the team description data from the NFL Verse.

    Parameters
    ----------
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("team_desc", force_refresh)


def get_officials(force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the officials data from the NFL Verse.

    Parameters
    ----------
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("officials", force_refresh)


def get_score_lines(force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the score lines data from the NFL Verse.

    Parameters
    ----------
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("score_lines", force_refresh)


def get_draft_picks(force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the draft picks data from the NFL Verse.

    Parameters
    ----------
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("draft_picks", force_refresh)


def get_combine(force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the combine data from the NFL Verse.

    Parameters
    ----------
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("combine", force_refresh)


def get_id_map(force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the ID map data from the NFL Verse.

    Parameters
    ----------
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("id_map", force_refresh)


def get_ngs(
    year: int,
    ngs_type: Literal["rushing", "passing", "receiving"],
    force_refresh: bool = False,
) -> pd.DataFrame:
    """
    Get the NGS data from the NFL Verse.

    Parameters
    ----------
    year : int
        The year to get the data for. Valid years are 2016 to the present.
    ngs_type : str
        The type of NGS data to get. Can be either "rushing", "passing", or "receiving".
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data(f"ngs", force_refresh, args={"year": year, "ngs_type": ngs_type})


def get_depth_chart(year: int, force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the depth chart data from the NFL Verse.

    Parameters
    ----------
    year : int
        The year to get the data for. Valid years are 2001 to the present.
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("depth_chart", force_refresh, args={"year": year})


def get_injuries(year: int, force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the injuries data from the NFL Verse.

    Parameters
    ----------
    year : int
        The year to get the data for. Valid years are 2009 to the present.
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("injuries", force_refresh, args={"year": year})


def get_qbr(
    level: Literal["nfl", "college"],
    freq: Literal["season", "weekly"],
    force_refresh: bool = False,
) -> pd.DataFrame:
    """
    Get the QBR data from the NFL Verse.

    Parameters
    ----------
    level : str
        The level of QBR data to get. Can be either "nfl" or "college".
    freq : str
        The frequency of QBR data to get. Can be either "weekly" or "season".
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("qbr", force_refresh, args={"level": level, "freq": freq})


def get_pfr(
    freq: Literal["season", "week"],
    s_type: Literal["pass", "rec", "rush", "def"],
    year: int,
    force_refresh: bool = False,
) -> pd.DataFrame:
    """
    Get the PFR data from the NFL Verse.

    Parameters
    ----------
    freq : str
        The frequency of PFR data to get. Can be either "week" or "season".
    s_type : str
        The type of PFR data to get. Can be either "pass", "rush", "def", or "rec".
    year : int
        The year to get the data for. Valid years are 2018 to the present.
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    if freq == "season":
        df = _get_data(
            f"pfr_season",
            force_refresh,
            args={"s_type": s_type},
        )

        # seasonal data requires filtering by year
        df = df[df["season"] == year]

        return df
    else:
        df = _get_data(
            f"pfr_week",
            force_refresh,
            args={"s_type": s_type, "year": year},
        )

        return df


def get_snap_counts(year: int, force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the snap counts data from the NFL Verse.

    Parameters
    ----------
    year : int
        The year to get the data for. Valid years are 2012 to the present.
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("snap_counts", force_refresh, args={"year": year})


def get_ftn(year: int, force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the FTN data from the NFL Verse.

    Parameters
    ----------
    year : int
        The year to get the data for. Valid years are 2022 to the present.
    force_refresh : bool
        If True, we automatically get the most up-to-date data from the NFL Verse and overwrite the local file.
    """
    return _get_data("ftn", force_refresh, args={"year": year})


PLAYER_NAME_MAP = {
    "Gary Jennings Jr": "Gary Jennings",
    "DJ Chark": "D.J. Chark",
    "Cedrick Wilson Jr.": "Cedrick Wilson",
    "Deangelo Yancey": "DeAngelo Yancey",
    "Ardarius Stewart": "ArDarius Stewart",
    "Calvin Johnson  HOF": "Calvin Johnson",
    "Mike Sims-Walker": "Mike Walker",
    "Kenneth Moore": "Kenny Moore",
    "Devante Parker": "DeVante Parker",
    "Brandon Lafell": "Brandon LaFell",
    "Desean Jackson": "DeSean Jackson",
    "Deandre Hopkins": "DeAndre Hopkins",
    "Deandre Smelter": "DeAndre Smelter",
    "William Fuller": "Will Fuller",
    "Lavon Brazill": "LaVon Brazill",
    "Devier Posey": "DeVier Posey",
    "Demarco Sampson": "DeMarco Sampson",
    "Deandrew Rubin": "DeAndrew Rubin",
    "Latarence Dunbar": "LaTarence Dunbar",
    "Jajuan Dawson": "JaJuan Dawson",
    "Andre' Davis": "Andre Davis",
    "Johnathan Holland": "Jonathan Holland",
    "Johnnie Lee Higgins Jr.": "Johnnie Lee Higgins",
    "Marquis Walker": "Marquise Walker",
    "William Franklin": "Will Franklin",
    "Ted Ginn Jr.": "Ted Ginn",
    "Jonathan Baldwin": "Jon Baldwin",
    "T.J. Graham": "Trevor Graham",
    "Odell Beckham Jr.": "Odell Beckham",
    "Michael Pittman Jr.": "Michael Pittman",
    "DK Metcalf": "D.K. Metcalf",
    "JJ Arcega-Whiteside": "J.J. Arcega-Whiteside",
    "Lynn Bowden Jr.": "Lynn Bowden",
    "Laviska Shenault Jr.": "Laviska Shenault",
    "Henry Ruggs III": "Henry Ruggs",
    "KJ Hamler": "K.J. Hamler",
    "KJ Osborn": "K.J. Osborn",
    "Devonta Smith": "DeVonta Smith",
    "Terrace Marshall Jr.": "Terrace Marshall",
    "Ja'Marr Chase": "JaMarr Chase",
}

COLLEGE_NAME_MAP = {
    "Ole Miss": "Mississippi",
    "Texas Christian": "TCU",
    "Central Florida": "UCF",
    "Bowling Green State": "Bowling Green",
    "West. Michigan": "Western Michigan",
    "Pitt": "Pittsburgh",
    "Brigham Young": "BYU",
    "Texas-El Paso": "UTEP",
    "East. Michigan": "Eastern Michigan",
    "Middle Tenn. State": "Middle Tennessee State",
    "Southern Miss": "Southern Mississippi",
    "Louisiana State": "LSU",
}
