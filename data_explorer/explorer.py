import sys

import pandas as pd
from IPython.core.display import display


class DataExplorer():
    def __init__(self, df):
        self.df = df


    def __repr__(self):
        r = pd.DataFrame(self.df.dtypes.value_counts())
        r.columns = ['']
        s =  "DataExplorer {}\n\n" + \
               "dtypes:\n{} \n\n" + \
               "memory usage: {} MB"
        return s.format(str(self.df.shape), r, self.size)


    @property
    def size(self):
        """Size of loaded DataFrame in MB"""
        return round(sys.getsizeof(self.df) / 1024 ** 2, 1)


    @property
    def na(self):
        """Percentage of null values for columns that have na"""
        missing = 100 * self.df.isna().mean()
        missing = missing[missing > 0]
        missing = round(missing, 1).sort_values(ascending=False)
        return missing


    @property
    def numerical(self):
        """Part of DataFrame that consists of number-type columns"""
        return self.df.select_dtypes(include=['number'])


    @property
    def other(self):
        """Part of DataFrame that consists of object-type columns"""
        return self.df.select_dtypes(include=['object'])


    @property
    def time(self):
        """Part of DataFrame that consists of datetime columns"""
        return self.df.select_dtypes(include=['datetime'])


    def unique(self, category_threshold=0, dropna=True):
        """Get number of unique values in each column by count and by percentage"""
        vals = self.df.nunique(dropna=dropna).sort_values(ascending=False)
        normalized = round(100 * (vals / self.df.shape[0]), 2)
        df = pd.DataFrame()
        df['unique'] = vals
        df['%'] = normalized
        if category_threshold:
            df = df.loc[df['unique'] > category_threshold]
        return df


    def count(self, col, dropna=False):
        """Count unique values for a column"""
        r = pd.DataFrame()
        r['counts'] = self.df[col].value_counts(dropna=dropna)
        r['%'] = round(100 * r['counts'] / len(self.df[col]), 2)
        return r


    def category(self, upper=10, lower=1, dropna=False):
        """Count unique values for columns that have {lower} < nunique < {upper}"""
        v = self.df.nunique(dropna=False)
        v = v[(v < upper) & (v > lower)]
        v = v.sort_values(ascending=False)
        for idx in v.index:
            d = self.count(col=idx, dropna=dropna)
            d.index.name = idx
            display(d)
            print()


    def bars(self, column, bins, step=False):
        """Get bins for a column
        If step is True return bins of that width"""
        if step:
            bins = int((self.df[column].max() - self.df[column].min()) / bins)
        return self.df[column].value_counts(bins=bins, sort=False)
