# Medida api-challenge
api challenge deliverable for medida

![API Flow](image.png)

## Steps to run this project:
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. docker-compose up --build

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







