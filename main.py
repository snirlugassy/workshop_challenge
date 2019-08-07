from data import ReutersData
import os
from classifiar import KNN
import article

if __name__ == "__main__":
    training_data_files = []
    for file in os.listdir("data"):
        training_data_files.append("data/" + file)

    training_data = ReutersData(["data/train.sgm"])
    data = training_data.get_data()

    testing_data = ReutersData(["data/testing.sgm"]).get_data()

    knn_classifiar = KNN(10)
    knn_classifiar.fit(data)

    for ar in testing_data:
        print("--")
        print(ar.tags)
        print(knn_classifiar.predict(ar))
        print("--")
