import sys
import math

maxDiff=[0,0,0,0,0,0]
minDiff=[0,0,0,0,0,0]

def prettyPrint(array):
    for each in array: print(each)
def formatInput(path):
    file = open(path, encoding="utf8")
    fileSplit = file.read().split("\n")
    data=[]
    global maxDiff, minDiff
    #CALCUALTE DIFFERENCE FOR EACH LINE, AND MAX/MIN DIFF
    for index, line in enumerate(fileSplit):
        if not(line[-2:]=='30' or line[-2:]=='00'): continue
        if (int(line[-8:-6])<8 or int(line[-8:-6])>19): continue
        if len(line)!=0 and line[0]=="#" or len(line)==0 or index==0: continue
        temp=[]
        lineSplit=line.split(";")
        #ITERATE EACH LINE
        invalid=False
        if abs(float(lineSplit[0])-float(lineSplit[2]))>=1:
            #print(lineSplit[0], lineSplit[2])
            invalid=True
            continue
        for i,each in enumerate(lineSplit):
            if index>=2 and i<6:
                #CALCULATE DIFFERENCE
                diff=round(float(fileSplit[index-1].split(";")[i])-float(each),2)
                #CHECK IF DATA INVALID
                if (i>=0 or i<=3) and abs(diff)>float(each)*0.1 or (i==4 or i==5) and abs(diff)>float(each)*0.3:
                    invalid=True
                    break
                temp+=[str(diff)]
                #NEW MIN/MAX DIFFERENCE
                if diff>maxDiff[i]:
                    maxDiff[i]=diff
                if diff<minDiff[i]:
                    minDiff[i]=diff
            #DONT READ LAST COLUMN
            elif i==len(lineSplit)-1 or index<2:
                continue
            else:
                temp+=[each]
        if invalid: continue
        #print(temp)
        data+=[";".join(temp)]
    print("MAXDIFF", maxDiff)
    print("MINDIFF", minDiff)
    return data

def writeData(data):
    file = open("train.txt", "w+")
    formatted="\n".join(data)
    file.write("temp1;humidity;temp2;pressure;co2;tvoc;window\n"+formatted)
    file2 = open("diff.txt", "a+")
    formatted=[]
    for i,each in enumerate(maxDiff):
        if i<6:
            d1=str(minDiff[i]); d2=str(round(minDiff[i]/3*2,2)); d3=str(round(minDiff[i]/3,2)); d4="0"
            d5=str(round(maxDiff[i]/3,2)); d6=str(round(maxDiff[i]/3*2,2)); d7=str(maxDiff[i])
            diffs=d1+"->"+d2+";"+d2+"->"+d3+";"+d3+"->"+d4+";"
            diffs+=d4+";"+d4+"->"+d5+";"+d5+"->"+d6+";"+d6+"->"+d7
            formatted+=[diffs]
    file2.write("\n".join(formatted))

def classifyData(data):
    global minDiff, maxDiff
    classified=[]
    #print(minDiff, maxDiff)
    for each in data:
        dataSplit=each.split(";")
        temp=[]
        for i, var in enumerate(dataSplit):
            if i==6: temp+=[var]; continue
            elif i>6: continue
            else: var=round(float(var),2)
            if var>=minDiff[i] and var<round(minDiff[i]/3*2,2): temp+=["["+str(minDiff[i])+"->"+str(round(minDiff[i]/3*2,2))+")"]
            elif var>=round(minDiff[i]/3*2,2) and var<round(minDiff[i]/3,2): temp+=["["+str(round(minDiff[i]/3*2,2))+"->"+str(round(minDiff[i]/3,2))+")"]
            elif var>=round(minDiff[i]/3,2) and var<0: temp+=["["+str(round(minDiff[i]/3,2))+"->"+"0"+")"]
            elif var==0: temp+=["[0]"]
            elif var>0 and var<=round(maxDiff[i]/3,2): temp+=["("+"0"+"->"+str(round(maxDiff[i]/3,2))+"]"]
            elif var>round(maxDiff[i]/3,2) and var<=round(maxDiff[i]/3*2,2): temp+=["("+str(round(maxDiff[i]/3,2))+"->"+str(round(maxDiff[i]/3*2,2))+"]"]
            elif var>round(maxDiff[i]/3*2,2) and var<=maxDiff[i]: temp+=["("+str(round(maxDiff[i]/3*2,2))+"->"+str(maxDiff[i])+"]"]
        classified+=[";".join(temp)]
    return classified

comArgs = sys.argv[:]
data=formatInput(comArgs[1])
#rettyPrint(data)
#writeData(data)
classified=classifyData(data)
writeData(classified)
