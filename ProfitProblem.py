from State import State
from Transition import Transition

class ProfitProblem:
    def __init__(self, time, plots, crops, validCrops, maxFallow, maxNonFallow, profit = lambda p, a, t: 0):
        self.time = time
        self.plots = plots
        self.crops = crops
        self.validCrops = lambda x : validCrops(x) + ["f"]
        self.maxFallow = maxFallow
        self.maxNonFallow = maxNonFallow
        self.profit = profit

    def succ(self, state):
        states = []
        if state.crop == "f":
            for c in self.crops:
                if c == "f":
                    states.append(State(c, min(state.fallow + 1, self.maxFallow), 0))
                else:
                    states.append(State(c, state.fallow, 1))
        else:
            states.append(State("f", 1, 0))
            if state.cultivation < self.maxNonFallow:
                for c in self.crops:
                    if c != "f":
                        states.append(State(c, state.fallow, state.cultivation + 1))
        return states

    def stateSets(self, p, t):
        if t <= 0:
            # return list(map(lambda c: State(c, 1 if c == "f" else 0, 0 if c == "f" else 1), self.validCrops(t)))
            return [State("f", self.maxFallow, 0)]
        else:
            states = []
            for state in self.stateSets(p, t - 1):
                states += filter(lambda s: s.crop in self.validCrops(t), self.succ(state))
            return list(set(states))

    def transitions(self, p, t):
        out = []
        if t == 0:
            return []
        for v in self.stateSets(p, t - 1):
            for v_ in self.stateSets(p, t):
                if v_ in self.succ(v):
                    out.append(Transition(v, v_))
        return out

    def transitionsPlus(self, p, t, v):
        return list(filter(lambda x: x.v1 == v, self.transitions(p, t + 1)))

    def transitionsMinus(self, p, t, v):
        return list(filter(lambda x: x.v2 == v, self.transitions(p, t)))