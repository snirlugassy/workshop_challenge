from data import ReutersData
import os
from classifiar import KNN
import article

TRAINING_DATA_PATH = "data/"

K = 25


def full_path(base, filename):
    if base[-1] != "/":
        base += "/"
    return base + filename


class Model:
    def __init__(self, path):
        training_data_files = []
        for root, _, files in os.walk(TRAINING_DATA_PATH):
            for name in files:
                training_data_files.append(os.path.join(root, name))

        training_data = ReutersData(training_data_files)

        self.classifiar = KNN(K)
        self.classifiar.fit(training_data.get_data())

    def predict(self, testing_data_path):
        testing_data_files = []
        for root, _, files in os.walk(testing_data_path):
            for name in files:
                testing_data_files.append(os.path.join(root, name))

        testing_data = ReutersData(testing_data_files).get_data()

        predictions = []
        ground_truth = []
        for ar in testing_data:
            ground_truth.append(ar.tags)
            predictions.append(tuple(self.classifiar.predict(ar)))
            print({"true": ar.tags, "predicted": predictions[-1]})

        return tuple(predictions)
