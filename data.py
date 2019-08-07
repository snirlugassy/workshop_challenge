import xmljson
from xml.etree import ElementTree
from html import unescape
import pickle
from article import Article

PICKLED_FILE_NAME = "training_data.pickle"


class ReutersData:
    def __init__(self, files=[]):
        self.data = []
        try:
            self.data = pickle.load(open(PICKLED_FILE_NAME, "rb"))
            print("pickle found")
            print(self.data)
        except (FileNotFoundError, pickle.UnpicklingError):
            # the data isn't pickled
            # load the data and pickle it!
            print("no pickle")
            for file in files:
                self.read_file(file)
            pickle.dump(self.data, open(PICKLED_FILE_NAME, "wb"))

    def read_file(self, path):
        with open(path, "r") as file:
            file.readline()
            data = unescape(file.read().replace("\n", " "))
            tree = ElementTree.fromstringlist(["<root>", data, "</root>"])
            parsed = xmljson.parker.data(tree)
            for doc in parsed["REUTERS"]:
                self.data.append(self.xml_to_article(doc))

    @staticmethod
    def xml_to_article(doc):
        try:
            title = doc["TEXT"]["TITLE"]
        except KeyError:
            title = ""

        try:
            text = doc["TEXT"]["BODY"]
        except KeyError:
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
