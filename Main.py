import gurobipy as gp

from ProfitProblem import ProfitProblem
from Crop import Crop
from Plot import Plot
from State import State

def myProfit(p, a, t):
    c = a.getTail().crop
    if c == "f":
        return 0
    elif c == "rice":
        return a.getTail().fallow * 2 * p.area
    elif c == "beans":
        return a.getTail().fallow * 3 * p.area
    else:
        return 0

def main():
    time = 5
    plots = [Plot(1), Plot(2), Plot(3)]
    crops = ["f", "rice", "beans"]
    validCrops = lambda x: ["beans" if x % 2 == 0 else "rice"]
    maxFallow = 3
    maxNonFallow = 3
    profit = myProfit
    prob = ProfitProblem(
        time,
        plots,
        crops,
        validCrops,
        maxFallow,
        maxNonFallow,
        profit
    )

    # Create a new model
    m = gp.Model()

    # Create variables
    xs = {}
    for p in plots:
        for t in range(time):
            transitions = prob.transitions(p, t)
            for a in transitions:
                x = m.addVar(vtype='B', name="x_{p}_{a}_{t}".format(p=plots.index(p), a=a, t=t))
                xs.update({(p, a, t): x})


    # Set objective function
    m.setObjective(sum(map(lambda x : xs[x] * profit(x[0], x[1], x[2]), xs.keys())), gp.GRB.MAXIMIZE)

    # Add constraints
    for p in plots:
        for t in range(1, time - 1):
            states = prob.stateSets(p, t)
            m.addConstr(sum(map(lambda a: xs[(p, a, t)], prob.transitions(p, t))) <= 1)
            for v in states:
                minusStates = prob.transitionsMinus(p, t, v)
                plusStates = prob.transitionsPlus(p, t, v)
                m.addConstr(sum(map(lambda a: xs[(p, a, t)], minusStates)) == sum(map(lambda a: xs[(p, a, t + 1)], plusStates)))

    # Solve it!
    m.optimize()
    for v in m.getVars():
        print('%s = %g' % (v.varName, v.x))

if __name__ == '__main__':
    main()