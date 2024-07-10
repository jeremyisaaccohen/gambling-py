## Casino

This is a little toy project to practice my TypeScript and some React/frontend work. 

## PreReqs
- **Poetry**: Make sure you have Poetry installed. You can install it from [here](https://python-poetry.org/docs/#installation).
- **Node.js and npm**: Make sure you have Node.js and npm installed. You can download them from [here](https://nodejs.org/).


## To run

Run `./start_casino.sh` from `gambling-py`. You may need to `chmod u+x start_casino.sh` to make it executable first.

I spent a bit more time than I was expecting just getting a cute shell script running that enabled SIGSTOP to stop both the front and backend processes. 

Alternatively, if you don't like executing semi-arbitrary shell scripts, you can run:
- `poetry install`
- `poetry run python gomboc_gambling/gambling.py`

And then in a separate terminal, just run:
- `npm install`
- `npm start`

