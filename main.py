import data
import os

if __name__ == "__main__":
    training_data_files = []
    for file in os.listdir("data"):
        training_data_files.append("data/" + file)

    reuters = data.ReutersData(training_data_files)
    data = reuters.get_data()
