# -*- coding: utf-8 -*-
import tushare as ts
import datetime as dt
import pandas as pd
import matplotlib


# init
end_str = '2015-07-17'

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
        ticks['dt'] = ticks['date'] + ' '+ ticks['time']
    return ticks


def cmp_top(ticks):
    if ticks is None:
        print 'no'
        return None
    try:
        today = ts.get_today_ticks(id).sort('amount', ascending=False)
    except:
        return None
    sticks = ticks.sort('amount', ascending=False).head(20)
    sticks = sticks.reset_index()
    today = today.reset_index()
    top = sticks.ix[0]
    top_today = today.ix[0]
    
    return [(round((top.price - top_today.price)/top.price, 3)), round(top.price, 3), round(top_today.price, 3), top.amount, top_today.amount]

rs = list()
cnt = 0
f = open('cmp.csv', 'w')
count = 0
for id in ts.get_stock_basics().index:
    count += 1
    print id
    cnt += 1
    ticks = get_ticks(id, end_str, 100)
    cmp = cmp_top(ticks)
    if cmp is None:
        continue
    cmp.append(id)
    print cmp
    if count % 5 == 0:
        f.flush()
    f.write(str(cmp) + '\n')
    rs.append(cmp)
f.close()

pd_ticks = pd.DataFrame(rs, columns=['rate', 'hist_price', 'today_price', 'hist-amount', 'today_amount', 'code'])
