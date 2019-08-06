import numpy as np

def cosine_sim(article1, article2):
    return np.dot(article1, article2)/(np.linalg.norm(article1)*np.linalg.norm(article2))

class KNN:
    def __init__(self, k, processed_data):
        self.k = k
        self.data = processed_data


#processed_data.articles   processed_data.tags


    def predict(self, new_article):

        for article in self.data.articles:


