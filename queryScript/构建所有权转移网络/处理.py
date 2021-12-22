import pandas as pd
import glob
import os

for file in glob.glob('./axie_transfer_data/*'):
    axie = pd.read_csv(file)
    file_name = os.path.basename(file)
    market_file = './market_buy_data/' + file_name
    market = pd.read_csv(market_file)
    total = pd.concat([market, axie], ignore_index=True)
    total = total.groupby(['from', 'to'])['times'].sum().reset_index(name='times')
    total.rename(columns={'from': 'Source', 'to': 'Target', 'times': 'Weight'}, inplace=True)
    total.to_csv('./total/{}'.format(file_name), index=False)
