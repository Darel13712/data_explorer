import pandas as pd
from IPython.core.display import display


class DataExplorer():
    def __init__(self, df):
        self.df = df

    @property
    def na(self):
        missing = round(100 * self.df.isna().mean(), 2)
        missing = missing[missing > 0].sort_values(ascending=False)
        return missing


    def unique(self, category_threshold=0, dropna=True):
        vals = self.df.nunique(dropna=dropna).sort_values(ascending=False)
        normalized = round(100 * (vals / self.df.shape[0]), 2)
        df = pd.DataFrame()
        df['unique'] = vals
        df['%'] = normalized
        if category_threshold:
            df = df.loc[df['unique'] > category_threshold]
        return df


    def category(self, upper=10, lower=1):
        v = self.df.nunique(dropna=False)
        v = v[(v < upper) & (v > lower)]
        v = v.sort_values(ascending=False)
        for idx in v.index:
            d = self.count(self.df.loc[:, idx])
            d.index.name = idx
            display(d.T)


    def hist(self, column, bins, step=False):
        if step:
            bins = int((self.df[column].max() - self.df[column].min()) / bins)
        return self.df[column].value_counts(bins=bins, sort=False)


    def count(self, col):
        r = pd.DataFrame()
        r['counts'] = self.df[col].value_counts(dropna=False)
        r['%'] = round(100 * r['counts'] / len(self.df[col]), 2)
        return r


    @property
    def numerical(self):
        return self.df.select_dtypes(include=['number'])


    @property
    def other(self):
        return self.df.select_dtypes(include=['object'])