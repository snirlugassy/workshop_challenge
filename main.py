import data

if __name__ == "__main__":
    parser = data.SGMLParser()
    with open("data/test.sgm") as sgm_file:
        print(sgm_file.readlines())
