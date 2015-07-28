import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import pandas.io.data as web
import matplotlib

hist = web.DataReader('bzun', "yahoo", dt.datetime(2014, 6, 1), retry_count=5, pause=0.1)
hist['code'] = 'bzun'
for name in ('aapl', 'goog', 'bidu', 'baba', 'qihu'):
    tmp = web.DataReader(name, "yahoo", dt.datetime(2014, 6, 1), retry_count=5, pause=0.1)
    tmp.code = name
    hist = hist.append(tmp)
