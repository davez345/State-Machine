class StateMachine:
    def __init__(self):
        self.startingState = None
        self.finiteState = None
        self.states = {}
        
    
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


lines = []
ntCount = 0
tCount = 0

nonTerminals = []
terminals = []
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
    nonTerminals.append(lines[j+1])
    #print(lines)
tCount = int(lines[ntCount+1])

for k in range(tCount):
    terminals.append(lines[ntCount+2+k])
ruleStart = ntCount + tCount +2

sm = StateMachine()
sm.startingState = nonTerminals[0]

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


print(sm.states)
