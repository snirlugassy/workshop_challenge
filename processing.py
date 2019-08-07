import math
import numpy as np
import article


class Processing:

    def __init__(self, articles):

        self.articles = articles

        self.words = {}

        self.df = {}

        self.numdocs = len(self.articles)

        self.stop_words = []

        self.create_stop_words_list()

        self.create_words_bank()

        self.inv_words = {v: k for k, v in self.words.items()}

        self.proccessed_articles = []

        self.build_train_set()


    def create_stop_words_list(self):

        with open('./stop_words.txt') as stop_words_file:

            for stop_word in stop_words_file:

                self.stop_words.append(stop_word.rstrip())

    def pre_process_word(self, word):

        word = word.rstrip(',.?!:')
        word = word.lower()

        if word in self.stop_words:

            return ''

        return word



    def create_words_bank(self):

        index = 0

        for art in self.articles:

                seen_in_this_article = []

                fullText = art.title + " " + art.text

                for word in fullText.split():

                    word = self.pre_process_word(word)

                    if word == '':

                        continue

                    if word not in self.df:

                        self.df[word] = 1  # document frequency

                        seen_in_this_article.append(word)

                    if word not in seen_in_this_article:

                        self.df[word] += 1

                        seen_in_this_article.append(word)

                    if word not in self.words.keys():  # if the word doesnt already exists in the words dictionary

                        self.words[word] = index  # add it

                        index += 1


    def build_train_set(self):

        for article in self.articles:
            vec = np.zeros(len(self.words))

            for word in article.title.split():

                    word = self.pre_process_word(word)

                    if word == '':

                        continue

                    vec[self.words[word]] += 2

            for word in article.text.split():

                word = self.pre_process_word(word)

                if word == '':
                    continue

                vec[self.words[word]] += 1

                for i in range(len(vec)):

                    if vec[i] == 0:
                        continue

                    vec[i] = (1 + math.log10(vec[i])) * math.log10(self.numdocs / self.df[self.inv_words[i]])

            self.proccessed_articles.append({'article': vec, 'tags': article.tags})


        return doc_set, reg_representation

    def parse_article(self, art):

        vec = np.zeros(len(self.words))

        for word in art.title.split():

            word = self.pre_process_word(word)

            if word == '':
                continue

            vec[self.words[word]] += 2

        for word in art.text.split():

            word = self.pre_process_word(word)

            if word == '':
                continue

            vec[self.words[word]] += 1

        for i in range(len(vec)):
            if vec[i] == 0:
                continue

            vec[i] = (1 + math.log10(vec[i])) * math.log10(self.numdocs / self.df[self.inv_words[i]])

        return vec
