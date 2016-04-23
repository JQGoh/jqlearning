""" train.csv file downloaded from
https://www.kaggle.com/c/predict-west-nile-virus/data """

import sys
sys.path.append("../bin/")
from data import DataIn

if __name__ == "__main__":
    train = DataIn("train.csv")
    train.summarize()
