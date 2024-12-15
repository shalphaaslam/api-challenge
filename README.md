# API-challenge
API challenge deliverable

API Flow:

![API Flow](image.png)

## Steps to run this project locally:
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. export FLASK_APP=events.py  # Linux/macOS
5. set FLASK_APP=events.py
6. flask run --host=0.0.0.0 --port=8000

## To use docker-compose:
docker-compose up --build

## To run testcases:
execute "pytest" in the terminal in the directory where your test script (events_test.py) is located.

You will find the api running in port 8000 in localhost

### Folders in the project:
uml:
Have diagrammatic representation of API Flow Using plantUML
Included api-flow.png exported from the api-flow code

api:
Have events.py, a flask app having API code implemented for the challenge.

event:
Have models required for api

test:
Unit tests created using pytest for the api code 







