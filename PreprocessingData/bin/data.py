#!usr/bin/env python

import pandas as pd
from preprocess import summary


class DataIn(object):
    """Represents an object which describes the imported data.

    Attributes:
        df: pandas.DataFrame
        fname: imported file name
        ftype: imported file type
    """
    def __init__(self, fname, ftype='csv'):
        """Create DataFrame from the imported file (default: CSV file type)."""
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

    def numeric(self, clean=True):
        """Convert the appropriate data to numeric type, and discard NaN.

        Args:
            clean: Boolean, if True cleaning all row entries if NaN found
                if False, no clearning of NaN
        """

        colnames = self.df.columns
        temp = self.df.apply(pd.to_numeric, args=('coerce',))
        removed = []
        for x in colnames:
            # Check columns which have all values as NaN
            if (temp[x].isnull().values.all()):
                removed.append(x)

        colnames = colnames.drop(removed)
        # Replace the text values with numeric values
        self.df[colnames] = temp[colnames]

        # Remove all row entries if presence of NaN found
        if clean:
            self.df = self.df.dropna()

    def summarize(self):
        """Provide the summary of your text and numeric data"""
        summary(self.df)
