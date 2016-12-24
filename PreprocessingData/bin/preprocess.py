#!usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

# Extract the numeric data in the fields of imported
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']


def summary(df):
    """Provide the summary of your text and numeric data.

    Parameters
    __________
    df: pandas.DataFrame.

    Outputs
    _______
    1) Summary of your text data using describe().
    2) Histogram of your numeric data.
    """
    print("-"*80)
    print("*"*20 + "    Begin of the summary of text data   " + "*"*20)
    print("-"*80)
    text_df = df.select_dtypes(exclude=numerics)
    for x in text_df.columns:
        print(text_df[x].describe())
        print("\n")

    print("-"*80)
    print("*"*20 + "    End of the summary of text data     " + "*"*20)
    print("-"*80)

    num_df = df.select_dtypes(include=numerics)
    num_df.hist(color='k', alpha=0.5, bins=50, figsize=(14, 14))

    plt.show()


def one2one(df):
    """Check if the given two columns of a data frame have values that
    are one-to-one correspondence.

    Parameters
    __________
    df: pandas.DataFrame that has two columns only.

    Returns:
    boolean: True if one-to-one correspondence found.
    """
    assert len(df.columns) == 2, "DataFrame does not have two columns"

    counts = []
    # check the unique mapping from the 1st column to the 2nd column
    # the relationship implies bidirectional mapping, if that is True
    group = df.groupby(df.columns[0])
    nums = group.transform(lambda x: len(x.unique()))
    counts.append(nums.values)

    # check whether the counts are 1 for each row
    if np.all(counts[0] == 1):
        return True
    else:
        return False
