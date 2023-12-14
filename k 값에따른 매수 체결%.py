import time
import pyupbit
import datetime
def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price
def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time
def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
start_time = get_start_time("KRW-BTC")
end_time = start_time + datetime.timedelta(days=1, hours=-2)
a = start_time - datetime.timedelta(hours=2)
now = datetime.datetime.now()


# k 값에따른 매수 체결 남은 % 계산기
k=0.1 #k값 초기  = 0.1
for i in range(7):
    target_price = get_target_price("KRW-BTC", k)  # 목표 매수가 계산
    current_price = get_current_price("KRW-BTC")  # 현재 시장가
    if k>0.3 and k<0.4:#오류떄매 넣음
        k=0.3
    print("K값            : ", k)
    print("오늘의 매수 가격 : ", target_price, "원")
    print("현재 가격       : ", current_price, "원")
    print("남은 가격       : ", target_price - current_price, "원")
    print("남은 %         : ", round(100 - (current_price * 100 / target_price), 3), "%\n")
    k +=0.1

