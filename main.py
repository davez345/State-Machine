class StateMachine:
    def __init__(self):
        self.startingState = None
        self.finiteState = None
        self.states = {}
        self.DKAstates = {}
        self.terminals = []
        self.nonTerminals = [] 
        
    
    def validate(self, string):
        print("sdasdas")


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

        print(len(self.DKAstates))

        for k, v in self.DKAstates.items():
            key = qDict[k]

            if(k == self.startingState):
                print(key + " I")
            elif("K" in k):
                print(key + " F")
            else:
                print(key)

        print(len(self.terminals))
        
        for t in self.terminals:
            print(t)

        for state, transitions in self.DKAstates.items():
            for transition, destination in transitions.items():
                print(qDict[state] + ", " + transition + ", " + qDict[destination])


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
    t = 0
    for c in chars:
        if c.islower():
            t += 1
    if(t > 1):
        return False        
    elif(not chars[len(chars)-1].islower()):
        return False
    return True


with open('gramatika.txt') as file:
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


for k in range(ruleStart, len(lines)):
    lineArr = lines[k].split()
    if(oldState != lineArr[0]):
        sm.states[lineArr[0]] = {}
        oldState = lineArr[0]


    for c in lineArr[0]:
        if c.islower():
            regular = False

    sm.addState(lineArr)
    
    if(len(lineArr[2]) > 1):
        regular = checkRight(lineArr[2])
    
    else:
        sm.states[lineArr[0]].update( { lineArr[2][0] : "K" })
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
    qDict[key] = "q"+str(i)
    i += 1

sm.saveDKA(qDict)

#print(sm.DKAstates)


