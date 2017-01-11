#!usr/bin/env python

import pandas as pd
from preprocess import summary, one2one
from itertools import combinations, chain


class DataIn(object):
    """Represents an object which describes the imported data.

    Attributes
    __________
    df: pandas.DataFrame.

    fname: str,
        imported file name.

    ftype: str,
        imported file type.
    """
    def __init__(self, fname):
        """Create DataFrame from the imported file.
        
        Parameters
        __________
        fname: str, 
            The filename of imported file.
        """
        try:
            ftype = fname[-4:]
            assert(ftype == '.csv')
            self.df = pd.read_csv(fname)
            self.fname = fname
            # Assume the file extension has three characters
            self.ftype = ftype
        except AssertionError:
            print("\nImported file type is not .csv!\n")
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

        Parameters
        __________
        clean: boolean, 
            True if cleaning all row entries where NaN found, False
            otherwise (no cleaning of NaN).
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
        """Provide the summary of your text and numeric data."""
        summary(self.df)

    def unique_sets(self):
        """Check the columns that share the same number of unique values.

        Returns
        _______
        dict: dict,
            Dictionary that contains the number of unique values as keys,
            features sharing the same set of number as values.

        Outputs
        _______
        Print out the number of unique values and their corresponding
        features.
        """
        colnames = self.df.columns
        uniq = {}
        for x in colnames:
            total = self.df[x].nunique()
            # Create a list to record the columns sharing the same number
            # of unique values
            if total not in uniq.keys():
                uniq[total] = []
                uniq[total].append(x)
            else:
                uniq[total].append(x)

        print("Number of unique values and their corresponding features")
        print(uniq)

        return uniq

    def one2one_sets(self):
        """Check the columns that share the same number of unique values.
        This function will check whether the unique values of a column will
        have one to one correspondence with other columns sharing the same
        number of unique values.

        Outputs
        _______
        Columns sharing the same unique values which have one-to-one
        correspondence, it available.
        """
        uniq = self.unique_sets()

        # keys: Total number of unique values. values: column names
        for k, v in uniq.items():
            if len(v) > 1:
                # Write a while loop to check all combination pairs
                while (len(v) >= 2):
                    warn = False
                    problems = []
                    for x in combinations(v, 2):
                        if not one2one(self.df[[x[0], x[1]]]):
                            warn = True
                            # Record the non one-to-one correspondence feature
                            problems.append(x)

                    # Break the while loop if all are one-to-one
                    if not warn:
                        break
                    # Remove common factors from v, and count the occurences
                    names = set(chain(*problems))
                    factors = dict([(x, 0) for x in names])
                    for x in problems:
                        factors[x[0]] += 1
                        factors[x[1]] += 1
                    # Select one of the features that repeats the most will work
                    factor = max(factors, key=factors.get)
                    v.remove(factor)

                if not warn:
                    print("Features {} have {} values which are one-to-one "
                          "correspondence.\n".format(v, k))
