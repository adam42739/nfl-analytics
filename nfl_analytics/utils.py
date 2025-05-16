class NflWeek:
    """
    A class to represent a week in the NFL season.
    """

    def __init__(self, season: int, week: int):
        self.season = season
        self.week = week

    def __str__(self):
        return f"{self.season} Week {self.week}"

    def __repr__(self):
        return f"NflWeek(year={self.season}, week={self.week})"
