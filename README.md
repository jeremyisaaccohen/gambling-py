
## Aside
Please note that the included README has been renamed as `project_requirements.md`

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



## Thoughts

I definitely don't have a ton of experience with front end dev work, so this was a bit of a fun exercise in that respect!

So while the routing wasn't too tricky after going through some documentation, I didn't bother adding CSS or any real styling, I hope that's sufficient for the back end role!

I also didn't have quite as much time to work on this as I hoped because I got stuck with physical therapy after tearing my ACL last week, so I'd be happy to talk about any improvements I would've made with more time or under differnet conditions.


## Thanks
Thanks for the opportunity thus far, and I hope to hear back from the team at Gomboc soon!