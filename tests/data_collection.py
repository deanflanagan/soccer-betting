from collections import defaultdict
import pandas as pd
import numpy as np
# https://bezkoder.com/node-js-express-sequelize-mysql/

# df = pd.read_csv('mls_data.csv', infer_datetime_format=True,parse_dates=['Date'])
#


def format_seasons(df):
    df.columns = map(str.lower, df.columns)

    # here we add additional columns we'll need for the strategy later

    df['hw'] = np.where(df.res == 'H', 1, 0)
    df['aw'] = np.where(df.res == 'A', 1, 0)
    df['x'] = np.where(df.res == 'D', 1, 0)

    # add the profit/loss for each bet type
    df['h_pl'] = np.where(df.hw == 1, df.ph - 1, -1)
    df['x_pl'] = np.where(df.x == 1, df.pd - 1, -1)
    df['a_pl'] = np.where(df.aw == 1, df.pa - 1, -1)

    # calculate overround. A fair value is 1... anything above is the bookies margin
    # ph represents pinnacle home... pinnacle being the most accurate bookie
    df['overround'] = df[['ph', 'pd', 'pa']].apply(lambda x: 1/x).sum(axis=1)

    # making a new temporary df with the fair odds
    fair_odds = df[['ph', 'pd', 'pa']].apply(
        lambda x: 1/df.overround/x).apply(pd.Series)
    fair_odds.columns = [x + 'f' for x in fair_odds.columns]

    # lets join them together...
    df = pd.concat([df, fair_odds], axis=1)

    # now lets show the differences between predictions
    # if a team is 80% to win, a win means the error is 20%. If a team was 25% to win, the err is 75%

    df['herr'] = np.where(df.hw == 1, df.phf, df.phf * -
                          1)  # abs(df.hw - df.phf)
    df['xerr'] = np.where(df.x == 1, df.pdf, df.pdf * -1)
    df['aerr'] = np.where(df.aw == 1, df.paf, df.paf * -1)

    # average of the err columns for all home & away teams
    df['herr_avg'] = df.herr.expanding(2).mean()
    df['aerr_avg'] = df.aerr.expanding(2).mean()

    # and drop everything we don't need
    df.drop(['maxh', 'maxd', 'maxa', 'avgh', 'avgd',
             'avga', 'country', 'league'], axis=1)

    # make sure we are sorted by date
    df.to_csv('test.csv', index=False)
    return df.sort_values('date')


if __name__ == "__main__":
    format_seasons(pd.read_csv(
        'mls_data.csv', infer_datetime_format=True, parse_dates=['Date']))
