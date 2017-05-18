""" DataIn class that can be used to load data .csv, followed by preprocessing"""

import pandas as pd
from preprocess import summary, one2one
from itertools import combinations, chain


class DataIn(object):
    """An object describing the imported data from .csv file

    Parameters
    ----------
    fname : str 
        The filename of imported .csv file.

    Attributes
    ----------
    df : pandas.DataFrame
        DataFrame which describes the data.

    fname : str
        Imported file name.

    ftype : str
        Imported file type, '.csv' in this case.
    """
    def __init__(self, fname):
        try:
            ftype = fname[-4:]
            assert(ftype == '.csv')
            self.df = pd.read_csv(fname)
            self.fname = fname
            self.ftype = ftype
        except AssertionError:
            print("\nImported file type is not .csv!\n")
            raise
        self.check()

    def check(self):
        """Check the  missing value or NaN (Not a Number) record found in the data.

        Inform the user if any missing values or NaN found in the data.
        """
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
        """Convert the features with partial numeric records to numeric type.

        Parameters
        ----------
        clean : boolean, default True
            If True, cleaning all row entries where NaN found.
            If False, no cleaning of row entries with NaN found. 
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
        """Provide the summary of your text and numeric data.

        This function calls preprocess.summary on imported DataFrame.
        """
        summary(self.df)

    def unique_sets(self):
        """Check the columns that share the same total number of unique values.

        Calling this function prints out the total number of unique values 
        and their corresponding features.

        Returns
        -------
        uniq : dict
            Dictionary with the total number of unique values as keys,
            features sharing the same set of number as values.
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

        print("-"*80)
        print("Number of unique values and their corresponding features")
        print("-"*80)
        for k in uniq.keys():
            print("Number of unique values: {}, Features: {}".format(
                k, uniq[k]))

        return uniq

    def one2one_sets(self):
        """Identify one to one correspondence relationship.

        Returns
        -------
        dict_one2one : dict
            Dictionary with sets of features which are one to one
            correspondence, if available. 
            Each set is grouped by the key of dictionary.
        """
        uniq = self.unique_sets()

        print('*'*10 + ' '*10 + "Conclusion for one to one correspondence" +
                " "*10 + "*"*10)
        # keys: Total number of unique values. values: column names
        for k, v in uniq.items():
            if len(v) > 1:
                pairs = []
                for x in combinations(v, 2):
                    if one2one(self.df[[x[0], x[1]]]):
                        pairs.append(x)

                # If no pair of features which are one to one correspondent
                if not pairs:
                    continue

                dict_one2one = {}
                dict_key = 1
                dict_one2one[dict_key] = set(pairs[0])
                for x in pairs[1:]:
                    new = True 
                    for key in dict_one2one.keys():
                        if (x[0] in dict_one2one[key]) or (
                                x[1] in dict_one2one[key]):
                            dict_one2one[key].add(x[0])
                            dict_one2one[key].add(x[1])
                            new = False
                            # If found within the old group, break from for loop
                            break
                    if new:
                        dict_key = dict_key + 1
                        dict_one2one[dict_key] = set(x)
               
                if dict_one2one:
                    for v in dict_one2one.values():
                        print("Features {} are one to one correspondence.".
                                format(v))
                return dict_one2one
