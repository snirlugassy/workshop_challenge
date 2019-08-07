import xmljson
from xml.etree import ElementTree
from html import unescape
import pickle
from article import Article
import re

PICKLED_FILE_NAME = "training_data.pickle"


class ReutersData:
    def __init__(self, files=[]):
        self.data = []
        try:
            with open(PICKLED_FILE_NAME, "rb") as pickle_file:
                self.data = pickle.load(pickle_file)
        except (FileNotFoundError, pickle.UnpicklingError):
            # the data isn't pickled
            # load the data and pickle it!
            for file in files:
                self.read_file(file)
            # pickle.dump(self.data, open(PICKLED_FILE_NAME, "wb"))

    def read_file(self, path):
        with open(path, "r", errors="ignore") as file:
            file.readline()
            sgml_raw_data = file.read().replace("\n", " ")
            # remove self closing tags
            # sgml_raw_data = re.sub(r'<.*/>', '', sgml_raw_data)
            data = unescape(sgml_raw_data)
            reuters_list = re.findall(r'(<\s*REUTERS.*?REUTERS\s*>)', data)
            for doc in reuters_list:
                try:
                    # parser = lxml.etree.XMLParser(ns_clean=True)
                    tree = ElementTree.fromstring(doc)
                    parsed = xmljson.parker.data(tree)
                    constructed_article = self.xml_to_article(parsed)
                    if len(constructed_article.tags) > 0:
                        self.data.append(constructed_article)
                except ElementTree.ParseError:
                    continue

    @staticmethod
    def xml_to_article(doc):
        try:
            title = doc["TEXT"]["TITLE"]
        except (KeyError, TypeError):
            title = ""

        try:
            text = doc["TEXT"]["BODY"]
        except (KeyError, TypeError):
            text = ""

        tags = set()
        labels_wrappers = ["TOPICS", "PLACES", "PEOPLE", "ORGS", "EXCHANGES", "COMPANIES"]
        for label in labels_wrappers:
            if label in doc.keys():
                try:
                    labels = doc[label]["D"]
                    if isinstance(labels, str):
                        tags.add(labels)
                        continue
                    if isinstance(labels, list):
                        tags = tags.union(set(labels))
                        continue
                except (KeyError, TypeError):
                    continue

        return Article(title, text, tags)

    def get_data(self):
        return self.data
