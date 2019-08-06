import numpy as np
from collections import OrderedDict
import article
def euclidean_dist(article1, article2):
    return np.linalg.norm(article1-article2)

class KNN:
    def __init__(self, k, processed_data):
        self.k = k
        self.data = processed_data


# processed_data[1]['article']   processed_data[1]['tags']

# new article is just numpy vector (not dict)


    def predict(self, new_article):

        list_dist = []
        list_sum_tags = []
        # change new article
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
        tags_dict = OrderedDict
        for article in relevant_data:
            for tag in article['tags']:
                tags_dict[tag] = tags_dict[tag]+1
        tags_to_ret = [k for k, v in sorted(tags_dict.items(), key=lambda x: x[1], reverse=True)]
        return tags_to_ret[:num_of_tags]





