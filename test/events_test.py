import datetime
from flask import Flask, jsonify
from api.events import get_events, fetch_nfl_events


# Create a pytest fixture for the Flask app
import pytest
from unittest.mock import patch
import requests

start_date = datetime.datetime.strptime('2024-05-01', '%Y-%m-%d').date()  # Convert string to datetime.date object
end_date = datetime.datetime.strptime('2024-05-05', '%Y-%m-%d').date()  # Convert string to datetime.date object

@pytest.fixture
def app():
    app = Flask(__name__)
    return app


def test_get_events_positive(app):
    start_date = datetime.datetime.strptime('2024-05-01', '%Y-%m-%d').date() 
    end_date = datetime.datetime.strptime('2024-05-05', '%Y-%m-%d').date()
    with app.test_request_context('/events', method='POST', json={'league': 'NFL', 'start_date': '', 'end_date': ''}):
        response = get_events()
        assert response is not None
        # assert isinstance(response, list)
        # assert len(response) > 0
        # Add more assertions based on expected response structure


@pytest.mark.xfail(reason="Expected to fail because The remote API responds even with no league or invalidLeague")
def test_get_events_negative(app):
    ## The remote API responds with no league or invalidLeague
    # Test with missing league parameter
    with app.test_request_context('/events', method='POST', json={'start_date': '', 'end_date': ''}):
        response = get_events()
        assert response is None

    # Test with invalid league parameter
    with app.test_request_context('/events', method='POST', json={'league': 'InvalidLeague', 'start_date': '', 'end_date': ''}):
        response = get_events()
        assert response is None


def test_fetch_nfl_events_positive():
    league = 'NFL'
    
    with patch('requests.get') as mock_get:
        # Mock scoreboard data response
        scoreboard_data = [
            {
                'id': '1',
                'timestamp': '2024-05-01T14:00:00Z',
                'away': {'id': 11, 'nickName': 'Away Team', 'city': 'Away City'},
                'home': {'id': 12, 'nickName': 'Home Team', 'city': 'Home City'}
            }
            # Add more sample scoreboard data entries as needed
        ]
        mock_get.return_value.json.return_value = scoreboard_data

        # Mock team rankings data response
        team_rankings_data = [
            {'teamId': 11, 'rank': 1, 'rankPoints': 100.0},
            {'teamId': 12, 'rank': 2, 'rankPoints': 90.0}
            # Add more sample team rankings data entries as needed
        ]
        mock_get.side_effect = [MockResponse(scoreboard_data), MockResponse(team_rankings_data)]

        events = fetch_nfl_events(league, start_date, end_date)
        assert events is not None
        assert isinstance(events, list)
        assert len(events) > 0
        # Add more assertions based on expected formatted event data


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")
