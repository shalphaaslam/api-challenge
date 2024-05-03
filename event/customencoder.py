# Author: Shalpha Aslam
# Description: This is a serializer class .
import json
from datetime import datetime
from api.events import Event  # Import your Event class

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, Event):
            return {
                "eventId": o.eventId,
                "eventDate": o.eventDate,
                "eventTime": o.eventTime,
                "homeTeamId": o.homeTeamId,
                "homeTeamNickName": o.homeTeamNickName,
                "homeTeamCity": o.homeTeamCity,
                "homeTeamRank": o.homeTeamRank,
                "homeTeamRankPoints": o.homeTeamRankPoints,
                "awayTeamId": o.awayTeamId,
                "awayTeamNickName": o.awayTeamNickName,
                "awayTeamCity": o.awayTeamCity,
                "awayTeamRank": o.awayTeamRank,
                "awayTeamRankPoints": o.awayTeamRankPoints
            }
        else:
            return super().default(o)
