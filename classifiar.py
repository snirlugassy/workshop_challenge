import numpy as np
from collections import OrderedDict
from processing import Processing
import pickle


def euclidean_dist(article1, article2):
    return np.linalg.norm(article1-article2)

PICKLED_PROCESSOR = "processor.pickle"
PICKLED_ARTICLES = "articles.pickle"

class KNN:
    def __init__(self, k):
        self.k = k
        self.data = []

    def fit(self, articles):
        try:
            with open(PICKLED_PROCESSOR, "rb") as processor_file:
                self.processor = pickle.load(processor_file)
                self.data = self.processor.proccessed_articles
                print("PICKLE WORKED!")
            # with open(PICKLED_ARTICLES, "rb") as known_articles_file:
            #     known_articles = pickle.load(known_articles_file)
            #     if known_articles == articles:
            #         with open(PICKLED_PROCESSOR, "rb") as processor_file:
            #             self.processor = pickle.load(processor_file)
            #             self.data = self.processor.proccessed_articles
            #             print("PICKLE WORKED!")
        except (FileNotFoundError, pickle.UnpicklingError):
            # the data isn't pickled
            # load the data and pickle it!
            print("NO PICKLE")
            self.processor = Processing(articles)
            self.data = self.processor.proccessed_articles

            with open(PICKLED_PROCESSOR, "wb") as processor_file:
                pickle.dump(self.processor, processor_file)
                print("CREATED PROCESSOR FILE")

            # with open(PICKLED_ARTICLES, "wb") as articles_file:
            #     pickle.dump(articles, articles_file)
            #     print("CREATED ARTICLES FILE")



    def predict(self, new_article):
        list_dist = []
        list_sum_tags = []
        new_article = self.processor.parse_article(new_article)
        for article in self.data:
            list_dist.append(euclidean_dist(new_article, article['article']))
            list_sum_tags.append(len(article['tags']))
        assert len(list_dist) == len(self.data)
        zipped = list(zip(list_dist, list_sum_tags, self.data))
        zipped.sort(key=lambda x: x[0])
        zipped = zipped[:self.k]
        list_sum_tags = (list(zip(*zipped)))[1]
        num_of_tags = round(sum(list_sum_tags)/self.k)
        relevant_data = (list(zip(*zipped)))[2]
        tags_dict = OrderedDict()
        for article in relevant_data:
            for tag in article['tags']:
                if tag in tags_dict.keys():
                    tags_dict[tag] += 1
                else:
                    tags_dict[tag] = 1
        tags_to_ret = [k for k, v in sorted(tags_dict.items(), key=lambda x: x[1], reverse=True)]
        return tags_to_ret[:num_of_tags]