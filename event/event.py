from datetime import datetime

class Event:
    def __init__(self, event_id, event_date, event_time, home_team_id, home_team_nickname, home_team_city,
                 home_team_rank, home_team_rank_points, away_team_id, away_team_nickname, away_team_city,
                 away_team_rank, away_team_rank_points):
        self.eventId = event_id
        self.eventDate = event_date
        self.eventTime = event_time
        self.homeTeamId = home_team_id
        self.homeTeamNickName = home_team_nickname
        self.homeTeamCity = home_team_city
        self.homeTeamRank = home_team_rank
        self.homeTeamRankPoints = home_team_rank_points
        self.awayTeamId = away_team_id
        self.awayTeamNickName = away_team_nickname
        self.awayTeamCity = away_team_city
        self.awayTeamRank = away_team_rank
        self.awayTeamRankPoints = away_team_rank_points

    @classmethod
    def from_scoreboard_data(cls, event_data, team_rankings_map):
        event_id = event_data["id"]
        event_datetime = datetime.strptime(event_data["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        event_date = event_datetime.strftime("%Y-%m-%d")
        event_time = event_datetime.strftime("%H:%M:%S")
        home_team_id = event_data["home"]["id"]
        home_team_nickname = event_data["home"]["nickName"]
        home_team_city = event_data["home"]["city"]
        home_rank, home_rank_points = team_rankings_map.get(home_team_id, (None, None))
        away_team_id = event_data["away"]["id"]
        away_team_nickname = event_data["away"]["nickName"]
        away_team_city = event_data["away"]["city"]
        away_rank, away_rank_points = team_rankings_map.get(away_team_id, (None, None))

        return cls(event_id, event_date, event_time, home_team_id, home_team_nickname, home_team_city,
                   home_rank, home_rank_points, away_team_id, away_team_nickname, away_team_city,
                   away_rank, away_rank_points)
