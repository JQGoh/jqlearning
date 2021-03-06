""" Functions for preprocessing data."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from itertools import combinations
from scipy.spatial.distance import cdist
# Extract the numeric data in the fields of imported
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']


def pair_dist(df1, df2, dict1, dict2):
    """Determine Euclidean distances between the values of selected
    features in DataFrames

    Parameters
    ----------
    df1: pandas.DataFrame

    df2: pandas.DataFrame

    dict1: dict
        key, value pair of dictionary
        key: Feature defines the groups
        value: List of features where the data are used for distance
        evaluation

    dict2: dict
        key, value pair of dictionary
        key: Feature defines the groups
        value: List of features where the data are used for distance
        evaluation

    Returns
    -------
    df: pandas.DataFrame
        DataFrame having columns from the key of dict2, index from
        the key of dict1
    """
    key1, val1 = list(dict1.items())[0]
    key2, val2 = list(dict2.items())[0]
    assert len(val1) == len(val2)
    pair_dist = cdist(df1[val1].values,
                      df2[val2].values)
    df = pd.DataFrame(data=pair_dist,
                      columns=df2[key2].values,
                      index=df1[key1].values)
    return df


def sets_grps(list1, list2):
    """Determine the sets of elements in both groups and their compositions

    Parameters
    ----------
    list1: list, or iterable

    list2: list, or iterable
    """
    set1 = set(list1)
    set2 = set(list2)
    print("Common elements in both sets:")
    common = set2.intersection(set1)
    print(common, len(common))
    print("\nElements of set1 not in set2:")
    set1_minus_set2 = set1 - set2
    print(set1_minus_set2, len(set1_minus_set2))
    print("\nElements of set2 not in set1:")
    set2_minus_set1 = set2 - set1
    print(set2_minus_set1, len(set2_minus_set1))


def grp_ts_scatter(df, time, feature, grp, col_wrap=4,
                   markersize=1.5, display_nan=False):
    """Time-series (date) scatter plots for a feature with respect to groups

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame of your data

    time: str
        Name that labels the time-series (datetime-like object)

    feature: str
        Feature name that we investigate the data distribution

    grp: str
        Column name that we separate the data with reference to

    col_wrap: int
        Number of columns in a row

    markersize: float
        Control the scatter spots' sizes

    display_nan: bool, default False
        If True, plot the missing values at zeroes in red
    """
    sns.set(style="darkgrid")

    # explicitly define the xlim, ylim
    ylim = (df[feature].min(), df[feature].max() )
    xlim = (df[time].min(), df[time].max())
    if display_nan:
        df_copy = nan_zeroes(df, feature)
        g = sns.FacetGrid(df_copy, col=grp, col_wrap=col_wrap,
                          xlim=xlim, ylim=ylim)
    else:
        g = sns.FacetGrid(df, col=grp, col_wrap=col_wrap,
                          xlim=xlim, ylim=ylim)

    g.map(plt.plot_date, time, feature, color="steelblue",
          markersize=markersize)
    if display_nan:
        g = g.map(plt.plot_date, time, "nan_" + feature,
                  color="red", markersize=markersize)

    g.set_xticklabels(rotation='vertical')
    plt.show()


def grp_hist(df, feature, grp, col_wrap=4, bins=50):
    """Histograms illustrate the data distribution of a feature with respect
       to groups

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame of your data

    feature: str
        Feature name that we investigate the data distribution

    grp: str
        Column name that we separate the data with reference to

    col_wrap: int
        Number of columns in a row

    bins: int
        Number of bins for histogram plot
    """
    sns.set(style="darkgrid")
    g = sns.FacetGrid(df, col=grp, col_wrap=col_wrap)
    g.map(plt.hist, feature, color="steelblue", bins=bins)
    plt.show()


def nan_zeroes(df, feature):
    """Add a new column with NaN in feature labelled as zeroes,
    other non-NaN will be labelled as NaN.

    Useful for graphical visualization of the distribution of missing values.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame of your data

    feature: str
        Feature name that we investigate the missing values

    Returns
    -------
    df_copy : pandas.DataFrame
        Data with outliers or non-outliers set to be np.nan
    """
    df_copy = df.copy()
    new_feature = "nan_" + feature
    # convert null to zeroes
    df_copy[new_feature] = np.isnan(df_copy[feature])
    df_copy[new_feature] = df_copy[new_feature].map(
        lambda x: 0 if x is True else np.nan)
    return df_copy


def outliers(df, col_names, low=0.05, high=0.95, outlier_as_nan=True):
    """Set ether outliers or non-outliers to be NaN

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame of your data

    col_names: list
        A list of column names where we shall remove the outliers

    low: float, default 0.05
        Values smaller than this quantile considered outliers

    high: float, default 0.95
        Values larger than this quantile considered outliers

    outlier_as_nan: boolean, default True
        If True, set outlier values to NaN
        If False, set non-outliers set NaN

    Returns
    -------
    df_copy : pandas.DataFrame
        Data with outliers or non-outliers set to be NaN
    """
    df_copy = df.copy(deep=True)
    lows = df[col_names].quantile(low)
    highs = df[col_names].quantile(high)
    for col in col_names:
        if outlier_as_nan == True:
            valid = df_copy[col].where(
                (df_copy[col] >= lows[col]) & (df_copy[col] <= highs[col]))
        else:
            valid = df_copy[col].where(
                (df_copy[col] < lows[col]) | (df_copy[col] > highs[col]))
        df_copy[col] = valid
    return df_copy


def summary(df, quantile=None, outlier_as_nan=True, filter_outlier=False):
    """Provide the summary of your text and numeric data.

    Calling this function provides the summary of text data using
    the built-in method describe() of pandas.DataFrame.
    Generate histogram plots for the numeric data.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame which describes the data

    quantile : tuple, default None
        tuple of (low, high) which refer to quantile range that we will
        not set the numeric values as outliers (NaN)

    outlier_as_nan: boolean, default True
        If True, set outlier values to NaN
        If False, set non-outliers set NaN

    filter_outlier: boolean, default True
        If True, histogram plot by filtering outliers
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

    if filter_outlier:
        num_df = outliers(num_df,
                          list(num_df.columns),
                          quantile[0],
                          quantile[1],
                          outlier_as_nan)
    
    # Suggest the layout for plotting
    num_fig_y = int(num_df.shape[1]/4) + 1
    num_df.hist(color='k', alpha=0.5, bins=50, figsize=(10, num_fig_y*2.5),
            layout=(num_fig_y, 4))
    plt.show()


def one2one(df):
    """Evaluate two columns of a DataFrame have one to one correspondence.

    Parameters
    ----------
    df : pandas.DataFrame, shape [n_samples, 2]

    Returns
    -------
    relation : boolean
        True, if one to one correspondence found.
    """
    assert len(df.columns) == 2, "DataFrame does not have two columns"

    counts = []
    # check the unique mapping from the 1st column to the 2nd column
    # the relationship implies bidirectional mapping, if that is True
    group = df.groupby(df.columns[0])
    nums = group.transform(lambda x: len(x.unique()))
    counts.append(nums.values)

    # check whether the counts are 1 for each row
    relation = False
    if np.all(counts[0] == 1):
        relation = True
    return relation


def warn_missing(df, fname=None):
    """Check the  missing value or NaN (Not a Number) record in data.

    Inform the user if any missing values or NaN found in the data.
    """
    warn = 0
    total_counts = df.shape[0]
    for x in df.columns:
        y = df[x]
        nan = y.index[y.isnull()]

        if nan.shape[0] != 0:
            warn = 1
            percentage = nan.shape[0]/total_counts*100
            print("Warning: Column {0} has ({1:.1f}%) {2:d}".format(
                x, percentage, nan.shape[0]),
                "missing values in {0}!".format(fname))

    if (warn == 0):
        print("No missing values in the columns of %s!\n" % fname)


def numeric(df, clean=True):
    """Convert the features with partial numeric records to numeric type.

    Parameters
    ----------
    clean : boolean, default True
        If True, cleaning all row entries where NaN found.
        If False, no cleaning of row entries with NaN found.

    Returns
    -------
    df_copy : pandas.DataFrame
        Data with features converted to numeric if relevant
    """
    df_copy = df.copy()
    colnames = df_copy.columns
    temp = df_copy.apply(pd.to_numeric, args=('coerce',))
    removed = []
    for x in colnames:
        # Check columns which have all values as NaN
        if (temp[x].isnull().values.all()):
            removed.append(x)

    colnames = colnames.drop(removed)
    # Replace the text values with numeric values
    df_copy[colnames] = temp[colnames]

    # Remove all row entries if presence of NaN found
    if clean:
        df_copy = df_copy.dropna()
    return df_copy


def unique_sets(df):
    """Check the columns that share the same total number of unique values.

    Calling this function prints out the total number of unique values
    and their corresponding features.

    Parameters
    ----------
    df : pandas.DataFrame
         Dataframe of our data

    Returns
    -------
    uniq : dict
        Dictionary with the total number of unique values as keys,
        features sharing the same set of number as values.
    """
    colnames = df.columns
    uniq = {}
    for x in colnames:
        total = df[x].nunique()
        # Create a list to record the columns sharing the same number
        # of unique values
        if total not in uniq.keys():
            uniq[total] = []
            uniq[total].append(x)
        else:
            uniq[total].append(x)

    print("-" * 80)
    print("Number of unique values and their corresponding features")
    print("-" * 80)
    for k in uniq.keys():
        print("Number of unique values: {}, Features: {}".format(
            k, uniq[k]))
    return uniq


def one2one_sets(df):
    """Identify one to one correspondence relationship.

    Parameters
    ----------
    df : pandas.DataFrame
         Dataframe of our data

    Returns
    -------
    dict_one2one : dict
        Dictionary with sets of features which are one to one
        correspondence, if available.
        Each set is grouped by the key of dictionary.
    """
    uniq = unique_sets(df)

    print('*' * 10 + ' ' * 10 + "Conclusion for one to one correspondence" +
          " " * 10 + "*" * 10)
    # keys: Total number of unique values. values: column names
    for k, v in uniq.items():
        if len(v) > 1:
            pairs = []
            for x in combinations(v, 2):
                if one2one(df[[x[0], x[1]]]):
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