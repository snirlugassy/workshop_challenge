# Reuter Article Class
class Article:
    def __init__(self, title, text, tags=[]):
        self.title = title
        self.text = text
        self.tags = tags

    def __cmp__(self, other):
        if self.title == other.title and self.text == other.text and self.tags == other.tags:
            return True
        return False
