
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
seaborn.set(style='ticks')


df = pd.read_json('data/bets.json')
df.home_bet.expanding().sum().plot().get_figure().savefig('plot.png')
