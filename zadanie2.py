'''
AFJ ZADANIE 2
David Zakharias
Terminaly: velke pismena
Neterminaly: male pismena a cisla 0-9
'''

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
    
    def validate_grammar(self, rules):
        valid = True
        epsilon = False
        for rule in rules:
            left = rule[0]
            right = rule[1]

            if(right[0] == "."):
                epsilon = True

            if(len(left) != 1 and (not left.isupper())):
                valid == False
            
           
            if(len(right) > 2):
                valid = False
   
            if(len(right) == 1 and (not right[0].islower() and not right[0].isdigit() and (right[0] != "."))):
                if(not (epsilon and right[0].isupper())):
                    valid = False
                    

        if(valid):
            print("Gramatika je regularna")
        else:
            print("Gramatika nie je regularna")
            exit(1)


        


    def validate(self, string):
        if(not string and len(self.startingState)>1):
            print("retazec je generovany DKA")
            exit(0)
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
        if("Q" in current):
            print("retazec je generovany DKA")
            exit(0)
        else:
            print("retazec nie je generovany DKA")
            exit(1)

    def read_grammar(self):
        readFile = sys.argv[1]
        lines = []
        i = 0

        with open(readFile) as file:
            for line in file:
                if(len(line)>1):
                    lines.append(line.rstrip())

        ntCount = int(lines[0])
        i += 1

        for j in range(ntCount):
            if(lines[i].isupper()):
                self.nonTerminals.append(lines[i])
                i += 1
            else:
                print("Nespravny pocet neterminalov")
                exit(1)
            #print(lines)
        tCount = int(lines[ntCount+1])
        i +=1

        for k in range(tCount):
            self.terminals.append(lines[i])
            i += 1

        

        #print(sm.nonTerminals)
        self.startingState = self.nonTerminals[0]

        state_lines = []

      
        for k in range(i, len(lines)):
            line_arr = lines[k].split("->")
            state_arr = [x.replace(' ','').strip(' ') for x in line_arr]
            state_lines.append(state_arr)
        
        
        self.insert_states(state_lines)
        self.validate_grammar(state_lines) 
        

    def insert_states(self, state_lines):
        
        current = ""
        epsilon = False       
       
        for state_arr in state_lines:

            if(state_arr[0] not in self.nonTerminals):
                print("Znak " + state_arr[0] + " sa nenachadza medzi neterminalmi gramatiky")
                exit(1)
          
            if(len(state_arr[1]) > 1):
                if (state_arr[1][0] not in self.terminals and state_arr[1][0] != "."):
                    print("Znak " + state_arr[1][0] + " sa nenachadza medzi terminalmi gramatiky")
                    exit(1)

            if(epsilon):
                if(len(state_arr[1]) == 1 and state_arr[1].isupper()):
                    if(current == "S" and current == state_arr[0]):
                        group = "S" + state_arr[1]
                        self.startingState = group
                        self.nonTerminals[0] = group
                        epsilon = False
                continue
                

          
            if(len(state_arr) > 1 and state_arr[1] == "."):
                current = state_arr[0]
                epsilon = True
                continue


            if(len(state_arr[1]) == 1):
                if((state_arr[1][0].islower() or state_arr[1][0].isdigit())):
                    state_arr[1] += "Q"

          

            if(state_arr[0] not in self.states):
               
                    self.states[state_arr[0]] = {}
                    stateList = []
                    stateList.append(state_arr[1][1])
                    self.states[state_arr[0]][state_arr[1][0]] = stateList
                    
            else:
                if(state_arr[1][0] not in self.states[state_arr[0]]):
                    stateList = []
                    stateList.append(state_arr[1][1])
                    self.states[state_arr[0]][state_arr[1][0]] = stateList
                else:
                    
                    self.states[state_arr[0]][state_arr[1][0]].append(state_arr[1][1])
          

    def create_dka(self):

        i = 0
        newStates = []
        newStates.append(self.startingState)
        
        while(i < len(newStates)):
            current = newStates[i]

            if(current not in self.DKAstates):
                self.DKAstates[current] = {}
            
            for t in self.terminals:
                st = ""
                for state in current:
                    if(state != "Q" and state in self.states):
                        if(t in self.states[state]):
                            for c in self.states[state][t]:
                                st += c
                if(st):
                    self.DKAstates[current][t] = st
                

                if(st not in newStates and st != ""):
                    newStates.append(st)
                
            i += 1


    def save_dka(self):
        print("[*] saving")
        saveFile = sys.argv[2]
        f = open(saveFile, "w")
        printSave(f,len(self.DKAstates))


        for k, v in self.DKAstates.items():
            key = k

            if(k == self.startingState):
                initial = key + " I"
                if(len(k) > 1):
                    initial = key + " IF"
                printSave(f,initial)
            

            elif("Q" in k):
                printSave(f,key + " F")
            else:
                printSave(f,key)

        printSave(f,len(self.terminals))
        
        for t in self.terminals:
            printSave(f,t)

        for state, transitions in self.DKAstates.items():
            for transition, destination in transitions.items():
                printSave(f,state + ", " + transition + ", " + destination)
    

sm = StateMachine()
sm.read_grammar()
sm.create_dka()
sm.save_dka()

string = input("Zadajte retazec na overenie: ")
sm.validate(string)
