from collections import defaultdict
import pandas as pd
import numpy as np

df = pd.read_csv('test.csv', infer_datetime_format=True, parse_dates=['date'])

# our betting strategy is based on the fact that market odds are ~ efficient
# if a team throws surprising results, the market will be wrong
# the more wrong over a few games means they will eventually revert
# we will see how betting on teams with x deviation (wrongness) after y games profits us... or not
# we can also hit an external api - Pinnacle sports - and get the odds for the next games
# we can then make the app bet automatically in future
# and we will notify of new bets via twilio


def add_bb_metrics(df, rolling_errs=4, min_games=6,):

    df['h_nth_game'] = np.nan
    df['a_nth_game'] = np.nan

    df['h_rolling_err'] = np.nan
    df['a_rolling_err'] = np.nan

    df['h_last_err'] = np.nan
    df['a_last_err'] = np.nan

    # rolling_errs = 4  # lets try the last 4 games
    # min_games = 6

    # for every team, make a list with their indices, err and if they were at home or no
    # then fill the columns with their game number
    # # and their err for the last x games
    # # and their err for their previous match

    # for x, y in enumerate(df.columns):
    #     print(x, y)
    all_seasons = []

    for season in df.season.unique():
        teams = {}
        data = df[df.season == season]

        for team in data.home.unique():
            teams[team] = []
            for match in data.to_records():
                if team == match[6]:  # team is home so add dict with home herr, index etc
                    teams[team].append(
                        {'id': match[0], 'err': match[-11]})

                    data.at[match[0], 'h_nth_game'] = len(teams[team]) - 1
                    if len(teams[team]) - 1 > min_games:
                        data.at[match[0], 'h_rolling_err'] = sum(
                            [x['err'] for x in teams[team]][-rolling_errs:-1])

                        data.at[match[0], 'h_last_err'] = [x['err']
                                                           for x in teams[team]][-2]

                elif team == match[7]:

                    teams[team].append(
                        {'id': match[0], 'err': match[-9]})
                    data.at[match[0], 'a_nth_game'] = len(teams[team]) - 1
                    if len(teams[team]) - 1 > min_games:
                        data.at[match[0], 'a_rolling_err'] = sum(
                            [x['err'] for x in teams[team]][-rolling_errs:-1])
                        data.at[match[0], 'a_last_err'] = [x['err']
                                                           for x in teams[team]][-2]

        all_seasons.append(
            data[(data['h_nth_game'] >= min_games) & (data['a_nth_game'] >= min_games)])

    pd.concat(all_seasons).to_csv('formatted.csv', index=False)
    return pd.concat(all_seasons)


add_bb_metrics(df)
