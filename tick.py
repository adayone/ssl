# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import tushare as ts
import datetime as dt
import pandas as pd
import matplotlib


# init
id = '600570'
end_str = '2015-07-16'

# get all time ticks
def get_ticks(id, end, delta):
    if isinstance(end, str):
        end = dt.datetime.strptime(end_str, '%Y-%m-%d')
    date_list = [end - dt.timedelta(days=x) for x in range(0, 100)]
    ticks = None
    for date in date_list:
        date_str = dt.datetime.strftime(date, '%Y-%m-%d')
        try:
            tick = ts.get_tick_data(id, date_str)
        except:
            continue
        if tick is None:
            continue
        tick['date'] = date_str
        if ticks is None:
            ticks = tick
        else:
            ticks = ticks.append(tick)
    return ticks


def cmp_top(ticks):
    if ticks is None:
        return None
    today = ticks.tail(1)
    sticks = ticks.sort('amount', ascending=False).head(20)
    sticks = sticks.reset_index()
    today = today.reset_index()
    top = sticks.ix[0]
    top_today = today.ix[0]
    
    return [round((top.price - top_today.price)/top.price, 3), top.price, top_today.price, top.amount, top_today.amount]


rs = list()
cnt = 0
for id in ts.get_stock_basics().index:
    print id
    cnt += 1
    ticks = get_ticks(id, end_str, 100)
    cmp = cmp_top(ticks)
    if cmp is None:
        continue
    cmp.append(id)
    print cmp
    rs.append(cmp)
    


pd_ticks = pd.DataFrame(rs, columns=['rate', 'hist_price', 'today_price', 'hist-amount', 'today_amount', 'code'])



