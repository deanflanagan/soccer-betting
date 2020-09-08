# Major League Soccer Betting API Documentation

This API generates bets on Major League Soccer for the discerning punter. Bet data is accessed from [here](https://www.football-data.co.uk/usa.php). Source data is csv and any data exchanged with the API is through json. Endpoints:

# Features

- [Python3](https://www.python.org/download/releases/3.0/) CLI
- Bespoke betting algorithm
- [Node.js](https://nodejs.org/) server
- Hosted [Postgres SQL](https://www.postgresql.org/) (using [Sequelize](http://sequelize.org/) ORM)
- Version control using [git](https://git-scm.com/)

# Installation

First, clone this project using:

```git
git clone https //github.com/spankyf/soccer-project
```

If you're running Anaconda, you should have everything installed. If not, cd into the folder where you cloned the project and run:

```python
pip install requirements.txt
```

For Node.js requirements, run:

```node
npm i
```

**Note:** You'll probably get this error on firing up the first time:

```
Error: { emitErrs } was removed in winston@3.0.0.
```

To fix, go to `winston\lib\winston\common.js` and remove (comment out) line 21 that says: ` throw new Error(format('{ %s } was removed in winston@3.0.0.', prop));`

## Python CLI

This CLI retrieves Major League Soccer matches, odds, results and dates. This data stretches back to 2012 and is used to model a betting strategy based on 'bouncebackability': mean reversion of a team to their expected market performance. The assumption here is the the market is more or less a trustworthy barometer to use for evaluating win probabilities.

## CLI Usage

Running `python make_bets.py` as is will provide a bets.json file using defaults yielding a juicy ~9% return since 2012.

You can pass the following arguments to `make_bets.py` to examine various strategies and results:

```python
python make_bets.py --rolling_errs=int
```

The rolling_errs integer sets the n last games the teams market underperformance to sum from.

```python
python make_bets.py --min_games=int
```

The minimum games from which to start calculating.

```python
python make_bets.py --cutoff_multi=float
```

The threshold number for which to decide to bet. You pass a positive number but the number is -ve in the model. A value of -2 represents a cumulative 200% underperformance over the last n rolling_errs (matches).

```python
python make_bets.py --stake=float
```

Add a representative stake. Nice if you want to see your actual monetary results.

**Note:** to understand full reasoning behind this strategy and decisions used, see the tests folder to find commented scripts.

# API Usage

To use, start the server using:

```node
npm run start
```

This API is set up as a RESTful API. After running the above script, go to `http://127.0.0.1/` in Postman and check out these results.

```
GET api/bets
```

Retrieve all made bets.
![Get all bets](public/readmePics/get_all_bets.png?raw=true "Get all bets")

```
POST api/bets
```

Make a new bet. Note the required parameters.
![Post bet](public/readmePics/post_new_bet.png?raw=true "Add a bet")

```
PUT api/bets/:id
```

Make a new bet. Note the required parameters.
![Update bet](public/readmePics/update_bet.png?raw=true "Update a bet")

```
DEL api/bets/:id
```

Delete a bet to massage your betting record...
![Delete bet](public/readmePics/delete_bet.png?raw=true "Delete a bet")

# Automatic Betting

I originally planned to have this algo automaticlly bet x minutes before start of match. This would have been achieved by accessing Pinnacle Sports API and betting through that:

```node
const request = require("request-promise");
const dotenv = require("dotenv");
dotenv.config({ path: "./config.env" });

exports.getOdds = function () {
  console.log("Got the odds");
  return request({
    method: "GET",
    uri:
      "https://api.pinnacle.com/v1/odds/special?sportId=24&specialId=1122578687&oddsFormat=Decimal",
    json: true,
    headers: {
      Authorization:
        "Basic " + new Buffer(process.env.PINNACLE_TOKEN).toString("base64"),
    },
  });
};
```

However they've since cut off my personal access to their API. So next...

# Upcoming features

- Use Twilio to send a reminder to a phone number x minutes before start of event to bet
- User controller & auth
- Deploy on Heroku to keep odds updating 'live'
