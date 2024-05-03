import json
import os
import sys
from flask import Flask, jsonify, request, abort, make_response

import requests
from datetime import datetime
import logging
from event.event import Event
from event.customencoder import CustomJSONEncoder
from urllib.parse import urljoin


app = Flask(__name__)

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set the logging level to INFO

# Create a console handler and set its log level to INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the console handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

@app.route('/events', methods=['POST'])
def get_events():
    # Handle POST request to retrieve NFL events
    # Logic to fetch events from remote API and format response
    payload = request.json
    league = payload.get('league')
    start_date = payload.get('start_date')
    end_date = payload.get('end_date')
    events = fetch_nfl_events(league, start_date, end_date)
    return events

def fetch_nfl_events(league, start_date=None, end_date=None):
    base_url = os.getenv('REMOTE_API_URL', 'http://172.18.0.1:9000')
    scoreboard_endpoint = f"/{league}/scoreboard"
    team_rankings_endpoint = f"/{league}/team-rankings"

    # Prepare query parameters for the scoreboard API request
    scoreboard_params = {}
    if start_date:
        scoreboard_params['since'] = start_date.strftime("%Y-%m-%d")
    if end_date:
        scoreboard_params['until'] = end_date.strftime("%Y-%m-%d")

    try:
        # Make GET request to retrieve NFL events data (scoreboard)
        scoreboard_url = urljoin(base_url, scoreboard_endpoint)
        logging.info(f"Making GET request to {scoreboard_url} with params {scoreboard_params}")
        scoreboard_response = requests.get(scoreboard_url, params=scoreboard_params)
        
        scoreboard_response.raise_for_status()
        scoreboard_data = scoreboard_response.json()
        logging.info("scoreboard_data: %s", scoreboard_data)


        team_rank_url = urljoin(base_url, team_rankings_endpoint)
        # Make GET request to retrieve team rankings data
        print(f"Making GET request to {team_rank_url}")
        team_rankings_response = requests.get(team_rank_url)
        team_rankings_response.raise_for_status()
        team_rankings_data = team_rankings_response.json()
        logging.info("team_rankings_data: %s", team_rankings_data)

        # Create a dictionary mapping team IDs to ranking data for quick lookup
        team_rankings_map = {team['teamId']: (team['rank'], team['rankPoints']) for team in team_rankings_data}
        logging.info("Team Rankings Map: %s", team_rankings_map)

        # Format the events data into the desired response format (EventsResponse schema)
        formatted_events = []
        for event_data in scoreboard_data:
            event = Event.from_scoreboard_data(event_data, team_rankings_map)
            formatted_events.append(event)

        # Create a response object
        response = make_response(json.dumps(formatted_events, cls=CustomJSONEncoder)) # Serialize using custom JSON encoder

        # Set the content type header to indicate JSON content
        response.headers['Content-Type'] = 'application/json'

        # Return the response
        return response
    

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection error, HTTP error)
        print(f"Error fetching NFL events: {e}")
        abort(400)  # Return 400 Bad Request

    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error parsing JSON response: {e}")
        abort(500) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 
