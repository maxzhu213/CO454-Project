class State:
    def __init__(self, crop, fallow = 0, cultivation = 0):
        self.crop = crop
        self.fallow = fallow
        self.cultivation = cultivation

    def __eq__(self, other):
        return self.crop == other.crop and self.fallow == other.fallow and self.cultivation == other.cultivation

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return "({crop}, {fallow}, {cultivation})".format(crop = self.crop, fallow = self.fallow, cultivation = self.cultivation)