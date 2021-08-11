class Transition:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def getHead(self):
        return self.v1

    def getTail(self):
        return self.v2

    def __repr__(self):
        return repr(self.v1) + ", " + repr(self.v2)

    def __eq__(self, other):
        return self.v1 == other.v1 and self.v2 == other.v2

    def __hash__(self):
        return hash(self.__repr__())