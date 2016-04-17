import sys
sys.path.append("../bin/")
from data import DataIn

if __name__ == "__main__":
    train = DataIn("train.csv")
    train.summarize()


