""" weather.csv file downloaded from
https://www.kaggle.com/c/predict-west-nile-virus/data """

import sys
sys.path.append("../bin/")
from data import DataIn

if __name__ == "__main__":
    weather = DataIn("weather.csv")
    weather.summarize()

    # Convert the data to numeric type and remove NaN entries
    weather.numeric()
    weather.summarize()
