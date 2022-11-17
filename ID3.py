import sys
import math
header=[]
headerDicts=[]
finishClause={}
entropy=1

branchesFinal=[]
formatted=[]

mostCommon_=""

def getEntropy(specs):
    e=0
    sum_=0
    for each in specs:
        sum_+=specs.get(each)
    for each in specs:
        p=specs.get(each)/sum_
        e-=p*math.log(p,2)
    return e

def getIG(eD, eSum, specs):
    ig=eD

    for each in specs:
        e=getEntropy(specs.get(each))
        sum_=0
        for num in specs.get(each):
            sum_+=specs.get(each).get(num)
        sum_=sum_/eSum
        ig-=sum_*e
    return ig

def bestIG(dataset, passed, eD2, sum2):
    tempDict={}
    for each in dataset:
        for i, spec in enumerate(each):
            name=header[i]
            if i==len(each)-1 or passed[i]!=0:
                continue
            if name not in tempDict:
                tempDict[name]={}
            if spec not in tempDict[name]:
                tempDict[name][spec]={}
            if each[-1] not in tempDict[name][spec]:
                tempDict[name][spec][each[-1]]=1
            else:
                tempDict[name][spec][each[-1]]+=1
    col=""
    best=-1
    ind=0
    for i, each in enumerate(tempDict):
        IG=getIG(eD2, sum2, tempDict.get(each))
        if IG>best:
            best=IG
            col=each
    for i, each in enumerate(header):
        if each==col:
            ind=i
            break
    return(ind)

def findFinishClauses(data):
    tempDict={}
    for each in data:
        if each[-1] not in tempDict:
            tempDict[each[-1]]=1
        else:
            tempDict[each[-1]]+=1
    return(tempDict)

def mostCommon(finishClause):
    maxNum=-1
    clause=""
    for each in finishClause:
        if finishClause.get(each)>maxNum or finishClause.get(each)==maxNum and each<clause:
            maxNum = finishClause.get(each)
            clause = each
    return clause

def tree(branches, clauses, eD, dataSet, column, passed, depth, limit):
    subDict={}
    nodes=headerDicts[column]
    passed[column]=1
    for each in nodes:
        dataset2=[]
        for row in dataSet:
            if row[column]==each:
                dataset2+=[row]
        global branchesFinal

        branches2=branches.copy()
        branches2[header[column]]=each

        finishClauses2=findFinishClauses(dataset2)

        if len(dataset2)==0:
            branches2[mostCommon_]=0
            branchesFinal+=[branches2]
            continue
        if depth+1>=limit:
            branches2[mostCommon(finishClauses2)]=0
            branchesFinal+=[branches2]
            continue
        if len(finishClauses2)==1:
            branches2[next(iter(finishClauses2))]=0
            branchesFinal+=[branches2]

            continue
        eD2=getEntropy(finishClauses2)
        sum2=len(dataset2)

        column2=bestIG(dataset2, passed, eD2, sum2)
        passed2=passed.copy()
        passed2[column2]=1

        tree(branches2, clauses, eD2, dataset2, column2, passed2, depth+1, limit)

def confusion(prediction, correct):
    global finishClause
    keys=sorted(finishClause.keys())
    keyDict={}
    matrix=[]
    for i,each in enumerate(keys):
        matrix.append([0 for each in keys])
        keyDict[each]=i
    for i,each in enumerate(prediction):
        matrix[keyDict[correct[i]]][keyDict[each]]+=1
    print("[CONFUSION_MATRIX]:")
    for each in matrix:
        print(*each)

def predict(data):
    prediction=[]
    correct=[]
    global formatted
    global mostCommon_
    guesses=0
    for each in data:
        correct.append(each[-1])
        match1=False
        for branch in formatted:
            match2=True
            for i, clause in enumerate(each):
                if branch[i]=='' or i==len(each)-1:
                    continue
                if branch[i]!=clause:
                    match2=False
                    break
            if match2:
                prediction.append(branch[-1])
                if branch[-1]==each[-1]:
                    guesses+=1
                match1=True
                break
        if not match1:
            prediction.append(mostCommon_)
            if mostCommon_==each[-1]:
                guesses+=1
    print("[PREDICTIONS]: ", end="")
    print(*prediction)
    print("[ACCURACY]: ", "{:0.5f}".format(guesses/len(prediction)))
    confusion(prediction, correct)
    return prediction

def prettyPrint(array):
    for each in array:
        print(each)

def formatBranches(branches, limit):
    global formatted
    global mostCommon_
    print("[BRANCHES]:")
    tempSet = set([])
    for each in branches:
        temp=["" for each in header]
        index=1
        i2=0
        toString=""
        for i,clause in enumerate(each):
            if i==len(each)-1:
                toString+=next(reversed(each.keys()))
                temp[-1]=next(reversed(each.keys()))
                continue

            toString+=str(index)+":"+header[header.index(clause)]+"="+each.get(clause)+" "
            temp[header.index(clause)]=each.get(clause)
            index+=1

        if toString not in tempSet:
            tempSet.add(toString)
            print(toString)
            formatted.append(temp)

def readInput(path):
    file = open(path, encoding="utf8")
    fileSplit = file.read().split("\n")
    data=[]
    global header
    global headerDicts

    index=0
    for line in fileSplit:
        if len(line)!=0 and line[0]=="#" or len(line)==0: continue
        temp=[]
        lineSplit=line.split(";")

        #SETUP HEADER
        if index==0:
            header=lineSplit.copy()
            for i, each in enumerate(lineSplit):
                if i==len(lineSplit)-1:
                    break
                headerDicts.append({})
            index+=1
            continue

        #FINISH CALUSE
        if lineSplit[-1] not in finishClause:
            finishClause[lineSplit[-1]]=0

        finishClause[lineSplit[-1]]+=1

        #ITERATE EACH LINE
        for i,each in enumerate(lineSplit):

            #DONT READ LAST COLUMN
            if i==len(header)-1:
                continue
            #IF NOT HEADER
            if index!=0:
                #CHECK IF SPEC ALREADY FOUND
                if each not in headerDicts[i]:
                    headerDicts[i][each]={}

                if lineSplit[-1] not in headerDicts[i][each]:
                    headerDicts[i][each][lineSplit[-1]]=0

                headerDicts[i][each][lineSplit[-1]]+=1

        index+=1
        data+=[lineSplit]
    return data

comArgs = sys.argv[:]


data=readInput(comArgs[1])

passed=[0 for each in header]

eD=getEntropy(finishClause)

IG=bestIG(data, passed, eD, len(data))

mostCommon_=mostCommon(finishClause)

limit=len(header)+1
if len(comArgs)==4:
    limit=int(comArgs[3])

tree({},finishClause, eD, data, IG, passed, 0, limit)


formatBranches(branchesFinal, int(limit))

#data2=readInput(comArgs[2])

#predictions=predict(data2)
