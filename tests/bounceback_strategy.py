from collections import defaultdict
import pandas as pd
import numpy as np

df = pd.read_csv('formatted.csv', infer_datetime_format=True,
                 parse_dates=['date'])

# lets start with this - 1.5 times the standard deviation which means they're underperforming
cutoff = - 1.5 * df.h_rolling_err.std()
# make sure they didn't bounce back the last game, anything < 0
last_game_max = 0

df['home_bet'] = np.where((df.h_rolling_err <= cutoff) & (
    df.h_last_err < last_game_max), df.h_pl, np.nan)

df['away_bet'] = np.where((df.a_rolling_err <= cutoff) & (
    df.a_last_err < last_game_max), df.a_pl, np.nan)


df.dropna(subset=df.columns[-2:], thresh=1).to_csv('bets.csv', index=False)
