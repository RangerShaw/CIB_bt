import pandas as pd
import math
import matplotlib.pyplot as plt


def read_data(fp):
    df = pd.read_excel(fp)
    t = df['价源发送时间'].astype(str).str.zfill(9)
    t = t.str[:6] + '.' + t.str[6:]
    df.insert(0, 'time', pd.to_datetime(df['价源发送日期'].astype(str) + ' ' + t))
    df = df.sort_values(by='time').reset_index(drop=True)
    return df


def clean_data(df):
    # drop irreverent data
    sdate = df['价源发送日期'].iloc[0].astype(str)
    edate = df['价源发送日期'].iloc[-1].astype(str)
    is_day = sdate == edate
    stime = pd.Timestamp(sdate + ' ' + ('09:00' if is_day else '20:00'))
    etime = pd.Timestamp(edate + ' ' + ('15:30' if is_day else '02:30'))
    df = df[df['time'].between(stime, etime)]
    return df


class Backtester:
    def __init__(self):
        self.mdata = pd.DataFrame
        self.is_day = bool
        self.stime = pd.Timestamp
        self.etime = pd.Timestamp

    def read_data(self, fp):
        df = pd.read_excel(fp)
        t = df['价源发送时间'].astype(str).str.zfill(9)
        t = t.str[:6] + '.' + t.str[6:]
        df.insert(0, 'time', pd.to_datetime(df['价源发送日期'].astype(str) + ' ' + t))
        df = df.sort_values(by='time').reset_index(drop=True)
        self.mdata = df
        return df

    def clean_data(self, df):
        sdate = df['价源发送日期'].iloc[0].astype(str)
        edate = df['价源发送日期'].iloc[-1].astype(str)
        self.is_day = sdate == edate
        self.stime = pd.Timestamp(sdate + ' ' + ('09:00' if self.is_day else '20:00'))
        self.etime = pd.Timestamp(edate + ' ' + ('15:30' if self.is_day else '02:30'))
        df = df[df['time'].between(self.stime, self.etime)]
        return df

    def analyze(self, freq, func):
        delta = pd.Timedelta(freq, 'm')
        n = math.ceil((self.etime - self.stime) / delta)
        intervals = [df[df['time'].between(self.stime + delta * i, self.stime + (i + 1) * delta)] for i in range(n)]
        results = pd.DataFrame([func(interval) for interval in intervals])
        return results

    def st_vol_one(self, df: pd.DataFrame):
        vb = df['申买量一'].value_counts().sort_index()
        va = df['申卖量一'].value_counts().sort_index()
        return vb.add(va, fill_value=0)


if __name__ == '__main__':
    test = Backtester()
    df = test.read_data("data/QuantHdsSgeBidPubOdmDeptExport_20230418_b.xlsx")
    test.clean_data(df)
    test.analyze(30, test.st_vol_one)
    # df = read_data("data/QuantHdsSgeBidPubOdmDeptExport_20230418_b.xlsx")
    # df = clean_data(df)
    # print(df)
    # df.set_index()
