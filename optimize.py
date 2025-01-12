# optimize.py
# this optimization algorithm aims to find the best set of weights to be applied to a set of parameters in order to minimize a cost function 
# inputs
# dataDic: dictionary of items with parameters to be weighted
# valueDic: dictionary of valued items
# noItemsForCostFunction: number of items to consider in the cost function  


import csv
import datetime


dataDic = {
    "aa": [9, 5, 10, 1, 2],
    "bb": [9, 6, 10, 1, 2],
    "cc": [9, 5, 2, 1, 2],
    "dd": [3, 3, 10, 1, 7],
    "ee": [9, 5, 1, 1, 2],
    "ff": [8, 5, 7, 3, 2],
    "gg": [8, 3, 7, 0, 2],
    "hh": [9, 5, 7, 0, 9],
    "ii": [7, 2, 10, 0, 7],
    "jj": [7, 3, 7, 5, 2],
    "kk": [2, 5, 10, 0, 4],
    "ll": [3, 2, 5, 0, 2],
    "mm": [9, 4, 5, 0, 2],
    "nn": [9, 2, 9, 0, 2],
    "oo": [9, 2, 5, 0, 8],
    "pp": [2, 7, 10, 0, 2],
    "qq": [9, 5, 3, 0, 2],
    "rr": [9, 1, 10, 3, 7],
    "ss": [9, 5, 10, 0, 3],
    "tt": [3, 5, 10, 0, 2],
    "uu": [2, 6, 10, 0, 7],
    "vv": [2, 5, 1, 4, 2],
    "ww": [2, 5, 10, 9, 2],
    "xx": [2, 5, 3, 4, 5],
    "yy": [2, 5, 10, 4, 9]
    }
    
valueDic = {
    "aa": 3,
    "bb": 4,
    "cc": 5,
    "dd": 4,
    "ee": 3,
    "ff": 3,
    "gg": 2,
    "hh": 3,
    "ii": 4,
    "jj": 5,
    "kk": 5,
    "ll": 0,
    "mm": 0,
    "nn": 1,
    "oo": 1,
    "pp": 2,
    "qq": 3,
    "rr": 4,
    "ss": 5,
    "tt": 5,
    "uu": 4,
    "vv": 3,
    "ww": 3,
    "xx": 3,
    "yy": 2
    }

noItemsForCostFunction = 6


def dbgout(string):
    if (debug == 1):
        print(string, file=traceFile)
    
def scoreFromInputs(key, dic, weights):
    score = dic[key][0] * weights[0] + dic[key][1] * weights[1] + dic[key][2] * weights[2] + dic[key][3] * weights[3] + dic[key][4] * weights[4]
    return score


def outputScore(targetNo, dataDic, weights, valueDic):
    # store individual scores in new dic
    rankingScores = {}
    for key in dataDic:
        rankingScores[key] = scoreFromInputs(key, dataDic, weights)
        # dbgout("score of %s: %s" % (key, rankingScores[key]))
    
    # sort by score values in ascending order
    sortedList = sorted(rankingScores.items(), key=lambda item: item[1], reverse=False)
    # dbgout("sorted list")
    names = ""
    
    # calculate compound score
    overallScore = 0
    for i, item in enumerate(sortedList):
        if i < targetNo:
            # add value of current item to value score
            value = valueDic[sortedList[i][0]]
            names += " " + sortedList[i][0]
            overallScore += value
        else:
            break
        dbgout("index: %d - item: %s - score: %s - total: %s - names: %s" % (i, item, value, overallScore, names))

    # return score
    return overallScore, names
    
def update(weights, index, delta):
    weights[index] = (weights[index] + delta) % 10 
    return weights

# returns tuple of optimal weights to minimize cumulated value of selected items
def optimize(noItems, inputDataDic, valueDic):
    # start with arbitrary weights:
    weights = [1, 1, 1, 1, 1]
    score = 10000000.0
    weightIndex = 0
    cnt = 0
    names = "none"
    
    while (1):
        cnt += 1
        newScore, newNames = outputScore(noItems, inputDataDic, weights, valueDic)
        if newScore <= score:
            print(newScore)
            print(newNames)
            print(weights)
            bestWeights = weights
            score = newScore
            names = newNames
            delta = 1
        else:
            # cycle weight index, simple heuristic, would deserve some improvement
            weightIndex = (weightIndex + 1) % 5
            delta = 7
        weights = update(weights, weightIndex, delta)
        dbgout(weights)
        
        # not sure we can identify there is one single attraction basin, better to iterate for some time
        if cnt == 1000000:
            break
    
    return bestWeights, score, names



# main
debug = False

 
# opening the file using "with" statement
# with open(filename,'r') as data:
   # for line in csv.reader(data):
       # print(line)
    
current_datetime = datetime.datetime.now()
ts = current_datetime.timestamp()

if debug == True:
    traceFile = open("optimize_log_%s.txt" % ts, 'w', encoding='utf-8')

w, s, n = optimize(noItemsForCostFunction, dataDic, valueDic)
print("best weights: ")
print(w)
print("score: %d" % s)
print("names: %s" % n)


    


