import pyupbit
import numpy as np

def get_ror(k,D):
    df = pyupbit.get_ohlcv("KRW-BTC", count= D)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

Date =730
print("최근 ",Date,"일 동안")
for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k,Date)
    print("k 값 : %.1f , 수익률 :  %.2f" % (k, (ror-1)*100),"%")