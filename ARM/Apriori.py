def loadDataSet():
    return [
        ['A', 'B', 'C', 'D'],
        ['A', 'B', 'C', 'D', 'E'],
        ['A', 'B', 'D'],
        ['A', 'B', 'E'],
    ]

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)

def scanD(dataSetList, CkSetList, minSupport):
    ssCnt = {}
    for transaction in dataSetList:
        for candidate in CkSetList:
            if candidate.issubset(transaction):
                if candidate not in ssCnt:
                    ssCnt[candidate] = 1
                else:
                    ssCnt[candidate] += 1
    retList = []
    supportData = {}
    numTransactions = float(len(dataSetList))
    for candidate in ssCnt:
        support = ssCnt[candidate] / numTransactions
        if support >= minSupport:
            retList.append(candidate)
        supportData[candidate] = support
    return retList, supportData

def apioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        L1 = list(Lk[i])[:k-2]
        L1.sort()
        for j in range(i+1, lenLk):
            L2 = list(Lk[j])[:k-2]
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)
    dataSetList = list(map(set, dataSet))
    L1, supportData = scanD(dataSetList, list(C1), minSupport)
    L = [L1]
    k = 2
    while len(L[k-2]) > 0:
        Ck = apioriGen(L[k-2], k)
        LK, supK = scanD(dataSetList, Ck, minSupport)
        supportData.update(supK)
        L.append(LK)
        k += 1
    return L, supportData

def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if i > 1:
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

def calcConf(freqSet, H, supportData, br1, minConf=0.7) :
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print(set(freqSet - conseq), '-->', set(conseq), 'support', supportData[freqSet], 'conf: ', conf)
            br1.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
    m = len(H[0])
    if len(freqSet) >= (m + 1):
        Hmp1 = calcConf(freqSet, H, supportData, br1, minConf)
        Hmp1 = apioriGen(Hmp1, m + 1)
        if len(Hmp1) > 1:
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)

if __name__ == "__main__":
    DataSet = loadDataSet()
    L, supportData = apriori(DataSet, minSupport=0.6)
    print (L)
    rules = generateRules(L, supportData, minConf=0.7)
