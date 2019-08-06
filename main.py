import data

if __name__ == "__main__":
    parser = data.SGMLParser()
    with open("data/test.sgm") as sgm_file:
        for line in sgm_file.readlines():
            pass
            # parser.feed(line)