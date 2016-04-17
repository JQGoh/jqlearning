#!usr/bin/env python

import pandas as pd
from preprocess import summary


class DataIn(object):
    """Represents an object which describes the imported data

    Attributes:
        df: pandas.DataFrame
        fname: imported file name
        ftype: imported file type
    """
    def __init__(self, fname, ftype='csv'):
        """Create DataFrame from the imported file (default: CSV file type)"""
        try:
            if (ftype == 'csv'):
                self.df = pd.read_csv(fname)
                self.fname = fname
                self.ftype = ftype
        except:
            print("Imported file type is not supported!")
            raise
        self.check()

    def check(self):
        """Checking the  missing values (NA or ,,)."""
        warn = 0
        for x in self.df.columns:
            y = self.df[x]
            nan = y.index[y.isnull()]
            if nan.shape[0] != 0:
                warn = 1
                print("Warning: Column %s has %d missing values in %s!" %
                      (x, nan.shape[0], self.fname))

        if (warn == 0):
            print("No missing values in the columns of %s!\n" % self.fname)

    def summarize(self):
        summary(self.df)
