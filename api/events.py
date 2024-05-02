import json
import os
import sys
from flask import Flask, jsonify, request, abort, make_response

import requests
from datetime import datetime
import logging
from event.event import Event
from event.customencoder import CustomJSONEncoder


app = Flask(__name__)

# Configure logging to write in log folder
logging.basicConfig(filename='api_logs.log', level=logging.INFO, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

# Add a stream handler to print logs on the console
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(handler)

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
    base_url = "http://172.18.0.1:9000"  # Replace the Ip address of the remote API
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
        logging.debug(f"Making GET request to {base_url + scoreboard_endpoint} with params {scoreboard_params}")
        scoreboard_response = requests.get(base_url + scoreboard_endpoint, params=scoreboard_params)
        scoreboard_response.raise_for_status()
        scoreboard_data = scoreboard_response.json()
        logging.debug("scoreboard_data: ", scoreboard_data)


        # Make GET request to retrieve team rankings data
        print(f"Making GET request to {base_url + team_rankings_endpoint}")
        team_rankings_response = requests.get(base_url + team_rankings_endpoint)
        team_rankings_response.raise_for_status()
        team_rankings_data = team_rankings_response.json()
        logging.debug("team_rankings_data: ", team_rankings_data)

        # Create a dictionary mapping team IDs to ranking data for quick lookup
        team_rankings_map = {team['teamId']: (team['rank'], team['rankPoints']) for team in team_rankings_data}
        logging.debug("Team Rankings Map: %s", team_rankings_map)

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
