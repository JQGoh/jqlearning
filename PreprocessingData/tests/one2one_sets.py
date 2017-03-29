""" train.csv and weather.csv files downloaded from
https://www.kaggle.com/c/predict-west-nile-virus/data """

import sys
sys.path.append("../bin/")
from data import DataIn
# from preprocess import one2one

if __name__ == "__main__":
    train = DataIn("train.csv")
    train.one2one_sets()

    corrupted = DataIn("train-corrupted.csv")
    corrupted.one2one_sets()

    weather = DataIn("weather.csv")
    weather.one2one_sets()
