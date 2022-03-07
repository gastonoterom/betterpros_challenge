# BetterPros Challenge

Simple chat application written in Python.

## Tech stack

- Python 3.9
- FastAPI
- SQLAlchemy
- SQLite
- JWT for token authentication

## Running the application

### Locally

- Install the dependencies: `pip install -r requirements.txt`
- Start the server: `uvicorn src.main:app`

### Docker

- Start the container: `docker run -d --name bp_challenge -p 8000:80 goterom/betterpros_challenge`

## Running the tests

- Install the dependencies: `pip install -r requirements.txt`
- Start testing: `python -m unittest -v`
