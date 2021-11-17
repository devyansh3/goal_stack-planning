import sys
# import nltk as nlp

init_state = [] # stores starting state given by the user initially
final_state = []  # stores final state to be achieved.
now_state = [] # used to store present state
planner = []   # used to store goal-planning
plan_formed = []  # used to store plan formed

# actions and predicates
# 4 types of actions include stack, pop, pickup by the arm, putdown
# stack : stores on top of it
# pop : remove from top 
# pickup : picks up the desired
# putdown : puts down 
actions = ["stack", "pop", "pickup", "putdown"]  
# 5 types of predicates : 
# on : BOX A ON BOX B
# clear :  CLEAR BLOCK
# arm_empty : ARM FREE TO FUNCTION
# on_table :  BOX ON TABLE
predicates = ["on", "clear", "arm_empty", "arm_holding", "on_table"]

# pre req for algos
# Preconditions append functions:- 
def preconditions_stack(X, Y):
    planner.append("holding "+str(X))
    planner.append("clear "+str(Y))
# Preconditions pop functions:- 
def preconditions_pop(X, Y):
    planner.append("on "+str(X)+" "+str(Y))
    planner.append("clear "+str(X))
# Preconditions pickup functions:-     
def preconditions_pickup(X):
    planner.append("arm_empty")
    planner.append("on_table "+str(X))                  
    planner.append("clear"+str(X))
    
# Preconditions putdown functions:-    
def preconditions_putdown(X):
    planner.append("holding "+str(X))

    
# Actions needed to fulfill the predicates
def for_on(X, Y):
    planner.append("stack "+str(X)+" "+str(Y))
    preconditions_stack(X, Y)
    
def for_ontable(X):
    planner.append("putdown "+str(X))
    preconditions_putdown(X)
    
def for_clear(X):
    
    # Finding the desired block on which X is stacked.
    check = "on "
    
    for position in now_state:
        if check in position:
            # splitting the position to fin
            temp_list = position.split()
            
            if temp_list[2] == X:
                break
            
    Y = str(temp_list[1])
    
    # Appending pop FUNCITON
    planner.append("pop "+str(Y)+" "+str(X))
    preconditions_pop(Y, X)
    
def for_armholding(X):
    check = "on_table "+str(X)
    
    if check in now_state:
        planner.append("pickup "+str(X))
        preconditions_pickup(X)
        
    else:
        # Finding the desired block on which X is stacked
        check = "on "
    
        for position in now_state:
            if check in position:
                # splitting the position to look for X
                temp_list = position.split()

                if temp_list[2] == X:
                    break

        Y = str(temp_list[1])

        # Appending pop FUNCTION
        planner.append("pop "+str(Y)+" "+str(X))
        preconditions_pop(Y, X)
        
def for_armempty():
    print("\nArm empty position false\n")
    sys.exit()
    
    
    
# CONSEQUENCES OF THE ACTIONS
def effect_stack(X, Y):
    now_state.remove("holding "+str(X))
    now_state.remove("clear "+str(Y))
    
    now_state.append("on "+str(X)+" "+str(Y))
    now_state.append("clear "+str(X))
    now_state.append("arm_empty")
    
def effect_pop(X, Y):
    now_state.remove("on "+str(X)+" "+str(Y))
    now_state.remove("clear "+str(X))
    now_state.remove("arm_empty")
    
    now_state.append("holding "+str(X))
    now_state.append("clear "+str(Y))
    
def effect_pickup(X):
    now_state.remove("arm_empty")
    now_state.remove("on_table "+str(X))
    now_state.remove("clear "+str(X))
    
    now_state.append("holding "+str(X))
    
def effect_putdown(X):
    now_state.remove("holding "+str(X))
    
    now_state.append("arm_empty")
    now_state.append("on_table "+str(X))
    now_state.append("clear "+str(X))
    


# # main algorithm
# forming a loop till the stack is not empty:
#   if position is found at the top of the stack and it is true:
#       pop the position from the stack
#   else : 
#           pop the position and push an action such that it satisfies that position onto stack  

# while stack is not empty: 
#  ;if top of stack is position: 
#  ; ;if position is true: 
#  ; ; ;pop it 
#  ; ;else:  
#  ; ; ;pop it 
#  ; ; ;push corresponding action that will satisfy that position onto stack 
#  ; ; ;push preconditions of that action 
#  ;if top of stack is action: 
#  ; ;pop it 
#  ; ;perform the action i.e add and delete it's effects from current state. 
#  ; ;add that action to the actual plan    
# # In[ ]:

# TAKING INPUT OF THE INITIAL STATE
input_string = input("Enter start state:- ")
# SPLITTING INITIAL STATE SEPARATED BY '-'
init_state = input_string.split("-")

# TAKING INPUT OF THE GOAL STATE
input_string = input("Enter goal state:- ")
# SPLITTING GOAL STATE SEPARATED BY '-'
final_state = input_string.split("-")

# PRINTING THE START AND GOAL STATE AS ENTERED BY THE USER
print("\nEntered Start State:- "+str(init_state))
print("\nEntered Goal State:- "+str(final_state)+"\n")










# PRESENT STATE
now_state = init_state.copy()



for position in final_state:
    planner.append(position)

# PRINTING THE PLANNING STACK AND CURRENT STATE TILL THE PLANNER IS EMPTY   
while len(planner) > 0:
    print("Planning Stack:- "+str(planner))
    print("Current State:- "+str(now_state)+"\n")
    
    top = planner.pop()
    temp = top.split()
    
    if temp[0] in predicates: # if position is present at the top of the stack
        
        if top in now_state: # if position found is true
            continue # it is already popped
            
        else: 
            
            # pushing the action to be performed to fulfill the position on the stack and pushing the necessary preconditions for that action.
            if temp[0] == "on":
                for_on(temp[1], temp[2])
            elif temp[0] == "on_table":
                for_ontable(temp[1])
            elif temp[0] == "clear":
                for_clear(temp[1])
            elif temp[0] == "arm_holding":
                for_armholding(temp[1])
            elif temp[0] == "arm_empty":
                for_armempty()
                
    if temp[0] in actions: # if action is present at the top of stack
        
        # execute the action by adding and deleting its effect from current state
        if temp[0] == "stack":
            effect_stack(temp[1], temp[2])
        elif temp[0] == "pop":
            effect_pop(temp[1], temp[2])
        elif temp[0] == "pickup":
            effect_pickup(temp[1])
        elif temp[0] == "putdown":
            effect_putdown(temp[1])
        
        # appending the action to the actual plan
        plan_formed.append(top)

# PRINTING THE FINAL CURRENT STATE AFTER NECESSARY OPERATIONS
print("Final Current State:- "+str(now_state))

# PRINTING THE CORRESPONDING PLAN GENERATED.       
print("\nPlan Generated:- \n")
for step in plan_formed:
    print(step)

# trial
# on B A-on_table A-clear B-arm_empty
# on A B-on_table B-clear A-arm_empty

# ques 1
# on B A-on_table A-on_table C-on_table D-clear B-clear C-clear D-arm_empty
# on C A-on B D-on_table A-on_table D-clear C-clear B-arm_empty
