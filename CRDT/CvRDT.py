class CvRDT:
    timestamp = 0
    dict = {}

    def join(self):
        print("join")

    def query(self):
        print("query")

    def merge(self):
        print("merge")

    def compare(self, read, local):
        if read < local:
            print(1)


class Entry:
    id = 0
    timestamp = 0
    data = None

