import data
import os

if __name__ == "__main__":
    training_data_files = os.scandir("data")
    parser = data.ReutersData(["data/test.sgm"])
