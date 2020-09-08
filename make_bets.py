from collections import defaultdict
import pandas as pd
import numpy as np
import sys
import argparse
import os
import matplotlib.pyplot as plt
import seaborn


def make_bets(rolling_errs=4, min_games=6,  cutoff_multi=0.5, year='all', stake=1):
    # if os.path.exists('data/raw_data.csv'):

    #     address = 'data/raw_data.csv'
    # else:
    address = 'https://www.football-data.co.uk/new/USA.csv'
    try:
        df = pd.read_csv(address)

    except Exception as e:
        print('uh oho')
        return e

    df.columns = map(str.lower, df.columns)

    df['hw'] = np.where(df.res == 'H', 1, 0)
    df['aw'] = np.where(df.res == 'A', 1, 0)
    df['x'] = np.where(df.res == 'D', 1, 0)

    df['h_pl'] = np.where(df.hw == 1, df.ph - 1, -1)
    df['x_pl'] = np.where(df.hw == 1, df.pd - 1, -1)
    df['a_pl'] = np.where(df.aw == 1, df.pa - 1, -1)

    df['overround'] = df[['ph', 'pd', 'pa']].apply(lambda x: 1/x).sum(axis=1)

    fair_odds = df[['ph', 'pd', 'pa']].apply(
        lambda x: 1/df.overround/x).apply(pd.Series)
    fair_odds.columns = [x + 'f' for x in fair_odds.columns]

    df = pd.concat([df, fair_odds], axis=1)
    df['herr'] = np.where(df.hw == 1, df.phf, df.phf * -
                          1)  # abs(df.hw - df.phf)
    df['xerr'] = np.where(df.x == 1, df.pdf, df.pdf * -1)
    df['aerr'] = np.where(df.aw == 1, df.paf, df.paf * -1)

    df['herr_avg'] = df.herr.expanding(2).mean()
    df['aerr_avg'] = df.aerr.expanding(2).mean()

    # df.drop(['maxh', 'maxd', 'maxa', 'avgh', 'avgd',
    #          'avga', 'country', 'league'], axis=1)

    df['h_nth_game'] = np.nan
    df['a_nth_game'] = np.nan

    df['h_rolling_err'] = np.nan
    df['a_rolling_err'] = np.nan

    df['h_last_err'] = np.nan
    df['a_last_err'] = np.nan

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

    df = pd.concat(all_seasons)

    cutoff = -cutoff_multi * df.h_rolling_err.std()

    last_game_max = 0  # additional parameter to make sure they didn't bounce back last match

    df['home_bet'] = np.where((df.h_rolling_err <= cutoff) & (
        df.h_last_err < last_game_max), df.h_pl, np.nan)

    df.dropna(subset=['home_bet'], thresh=1, inplace=True)

    df['home_bet'] = df['home_bet'] * stake
    df['unbet'] = np.where(df.hg.isnull(), 1, 0)
    df['odds'] = df['ph']
    if year != 'all':
        df = df[df.season == year]

    kept_labels = ['date', 'home', 'away', 'odds', 'home_bet', 'unbet', 'time']
    df.drop(labels=[x for x in df.columns if x not in kept_labels],
            axis=1, inplace=True)
    df.to_json(path_or_buf='data/bets.json', orient='records')
    df.home_bet.expanding().sum().plot().get_figure().savefig('data/plot.png')
    print('Python message - bet history made with graph')
    # df.to_csv('finished.csv', index=False)
    # print(df.home_bet.describe())
    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Betting on MLS home teams due to bounce back from poor form')
    parser.add_argument('--rolling_errs', type=int,
                        help='N of last games played to sum for err')
    parser.add_argument('--min_games', type=int,
                        help='Min games played before strategy started')
    parser.add_argument('--cutoff_multi', type=float,
                        help='Negative stdev to use for calculation. Larger is more conservative, max 2.5')
    parser.add_argument('--year', type=int,
                        help='Filter by season integer')
    parser.add_argument('--stake', type=float,
                        help='Your stake in $')

    parser.set_defaults(rolling_errs=6, min_games=6, cutoff_multi=1.5)
    args = parser.parse_args()
    make_bets(rolling_errs=args.rolling_errs,
              min_games=args.min_games, cutoff_multi=args.cutoff_multi)
