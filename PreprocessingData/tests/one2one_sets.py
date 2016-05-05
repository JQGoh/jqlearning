""" train.csv file downloaded from
https://www.kaggle.com/c/predict-west-nile-virus/data """

import sys
sys.path.append("../bin/")
from data import DataIn
# from preprocess import one2one

if __name__ == "__main__":
    train = DataIn("train-corrupted.csv")
    train.one2one_sets()
    train = DataIn("train.csv")
    train.one2one_sets()


    weather = DataIn("weather.csv")
    weather.one2one_sets()
