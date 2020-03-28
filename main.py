import sys,getopt

def printSave(f, string):
        f.write(str(string)+"\n")
        print(str(string))

class StateMachine:
    def __init__(self):
        self.startingState = None
        self.finiteState = None
        self.states = {}
        self.DKAstates = {}
        self.terminals = []
        self.nonTerminals = [] 
    
    def validate(self, string):
        current = self.startingState
        for c in string:
            if(c not in self.terminals):
                print("retazec nie je generovany DKA")
                exit(1)
            if(c in self.DKAstates[current]):
                current = self.DKAstates[current][c]
            else:
                print("retazec nie je generovany DKA")
                exit(1)
        if("K" in current):
            print("retazec je generovany DKA")
        else:
            print("retazec nie je generovany DKA")
            exit(1)




    def addState(self, lineArr):
        if(len(lineArr[2]) == 1):
            lineArr[2] += "K"

        if(lineArr[2][0] not in self.states[lineArr[0]]):
            stateList = []
            print(lineArr[2][1])
            stateList.append(lineArr[2][1])
            self.states[lineArr[0]].update( { lineArr[2][0] : stateList} )
        else:
            self.states[lineArr[0]][lineArr[2][0]].append(lineArr[2][1])


    
    

    def saveDKA(self, qDict):

        saveFile = sys.argv[2]
        f = open(saveFile, "w")
        printSave(f,len(self.DKAstates))


        for k, v in self.DKAstates.items():
            key = qDict[k]

            if(k == self.startingState):
                printSave(f,key + " I")
            elif("K" in k):
                printSave(f,key + " F")
            else:
                printSave(f,key)

        printSave(f,len(self.terminals))
        
        for t in self.terminals:
            printSave(f,t)

        for state, transitions in self.DKAstates.items():
            for transition, destination in transitions.items():
                printSave(f,qDict[state] + ", " + transition + ", " + qDict[destination])


    def createDKA(self):
        end = False
        newStates = []
        newStates.append(self.startingState)
        i = 0

        while(not end and i != len(newStates)):
            end = True
            current = newStates[i]
            i += 1 
            self.DKAstates[current] = {} 
            for c in current:
                currentNt = c
                
                for t in self.terminals:
                    newState = ""
                    if(currentNt != "K" and t in self.states[currentNt]):
                        #print(currentNt + "/" + t)
                        for state in self.states[currentNt][t]:
                            newState += state
                        #print(newState)
                        self.DKAstates[current].update({ t : newState })

                        if(newState not in newStates):
                            newStates.append(newState)
                            #print(newState)
                            end = False
                    if(currentNt == "K"):
                        end = False
        
lines = []
ntCount = 0
tCount = 0
sm = StateMachine()


rules = {}
regular = True

def checkRight(chars):

    if(len(chars) > 2):
        return False
    else:
        if(chars[0].islower() and chars[1].isupper()):
            return True
        else:
            return False
    return True
 

readFile = sys.argv[1]


with open(readFile) as file:
    for line in file:
        lines.append(line.rstrip())

ntCount = int(lines[0])

for j in range(ntCount):
    sm.nonTerminals.append(lines[j+1])
    #print(lines)
tCount = int(lines[ntCount+1])

for k in range(tCount):
    sm.terminals.append(lines[ntCount+2+k])
ruleStart = ntCount + tCount +2

#print(sm.nonTerminals)
sm.startingState = sm.nonTerminals[0]

oldState = ""


for k in range(ruleStart, len(lines)-2):


    lineArr = lines[k].split("->")
    lineArrNew = [x.replace(' ','').strip(' ') for x in lineArr]
    lineArr = []
    lineArr.append(lineArrNew[0])
    lineArr.append("->")
    print(lineArrNew)
    lineArr.append(lineArrNew[1])
    

    if(oldState != lineArr[0]):
        sm.states[lineArr[0]] = {}
        oldState = lineArr[0]


    if(len(lineArr[0]) == 1):
        if lineArr[0].islower():
            regular = False
    else:
        regular = False

    sm.addState(lineArr)
    
    if(len(lineArr[2]) > 1):
        regular = checkRight(lineArr[2])
    
    else:
        
        if(lineArr[2].isupper()):
            regular = False
        
    rules[lineArr[0]] = lineArr[2]

if(not regular):
    print("gramatika nie je regularna")
else:
    print("gramatika je regularna")

#print(nonTerminals)
#print(terminals)

#print(sm.states)
#print("="*40)
sm.createDKA()

qDict = {}
i = 0

#print(len(sm.DKAstates))

for key in sm.DKAstates:
    qDict[key] = "q" + str(i)
    i += 1

sm.saveDKA(qDict)
while(1):
    toValidate = input("Zadaj retazec na overenie: ")
    sm.validate(toValidate)



#print(sm.DKAstates)


