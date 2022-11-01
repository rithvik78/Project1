import copy # to make a copy of child 
import time # to measure the time of algorithm 

# Data structure that is used to store the puzzle 
class Node:
    def __init__(self,puzzle,cost,depth):
        self.puzzle = puzzle
        self.cost = cost
        self.depth = depth

# some of the default puzzles that can be used for testing the algorithm 
default_puzzle ={
                    '1':[[1,2,3],[4,5,6],[7,8,0]],
                    '2':[[1,2,3],[4,5,6],[0,7,8]],
                    '3':[[1,2,3],[5,0,6],[4,7,8]],
                    '4':[[1,3,6],[5,0,2],[4,7,8]],
                    '5':[[1,3,6],[5,0,7],[4,8,2]],
                    '6':[[1,6,7],[5,0,3],[4,8,2]],
                    '7':[[7,1,2],[4,8,5],[6,3,0]],
                    '8':[[0,7,2],[4,6,1],[3,5,8]]
                }
# goal state of the puzzle 
goalPuzzle = [[1,2,3],[4,5,6],[7,8,0]]

# function that finds if the numbers match with the goal state puzzle 
def isValid(puzzle,val):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j]==val:
                return i,j
    return -1,-1 # returns -1 if the puzzle match fails 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Functions for the movements of the blank space in the puzzle 
# Basically swaps the numbers 

def down(root:Node):
    x,y=isValid(root.puzzle,0)
    if x!=0:
        root.puzzle[x][y],root.puzzle[x-1][y]=root.puzzle[x-1][y],root.puzzle[x][y]
        return root
    else:
        return None

def left(root:Node):
    x,y=isValid(root.puzzle,0)
    if y!=2:
        root.puzzle[x][y],root.puzzle[x][y+1]=root.puzzle[x][y+1],root.puzzle[x][y]
        return root
    else:
        return None

def right(root:Node):
    x,y=isValid(root.puzzle,0)
    if y!=0:
        root.puzzle[x][y],root.puzzle[x][y-1]=root.puzzle[x][y-1],root.puzzle[x][y]
        return root
    else:
        return None

def up(root:Node):
    x,y=isValid(root.puzzle,0)
    if x!=2:
        root.puzzle[x][y],root.puzzle[x+1][y]=root.puzzle[x+1][y],root.puzzle[x][y]
        return root
    else:
        return None

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def misplacedTile(root:Node):
    s=0
    for i in range(len(root.puzzle)):
        for j in range(len(root.puzzle[i])):
            if goalPuzzle[i][j]!=root.puzzle[i][j] and all(v!=len(root.puzzle[i])for v in (i,j)):
                s+=1
    return s

def manhattanDistance(root:Node): # https://www.geeksforgeeks.org/sum-manhattan-distances-pairs-points/
    s=0
    for i in range(len(root.puzzle)):
        for j in range(len(root.puzzle[i])):
            x,y=isValid(goalPuzzle,root.puzzle[i][j])
            if root.puzzle[i][j]!=0:
                s+=abs(x-i)+abs(y-j)
    return s

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# general-search Algorithm
def generalSearch(root: Node, queue_function): # refered from the lecture slides 
    nodes = [root] # nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
    maxi=0 # to update the counter used for loop 
    cnt=0 # count of nodes expanded 
    
    while len(nodes)!=0:
    
        node=nodes.pop(0)
        if node.puzzle == goalPuzzle:
            print('successfull'+' '+str(cnt))
            return node
        nodes=queue_up(node,nodes,queue_function)        
        cnt+=1
        if maxi<len(nodes):
            maxi=len(nodes)
    
    print('no result')
    return None

def queue_up(node,nodes,queue_function):
    global abc # visited states made global to avoid confusion 
    x=copy.deepcopy(node)
    x=up(x)
    if x is not None:
        x.depth=node.depth+1
        if queue_function=='1':
            x.cost=x.depth + 0
        elif queue_function=='2':
            x.cost=x.depth+misplacedTile(x)
        elif queue_function=='3':
            x.cost=x.depth+manhattanDistance(x)
        if [x.cost,x.puzzle] not in abc:
            nodes.append(x)
            abc.append([x.cost,x.puzzle])
    x=copy.deepcopy(node)
    x=down(x)
    if x is not  None:
        x.depth=node.depth+1
        if queue_function=='1':
            x.cost=x.depth + 0
        elif queue_function=='2':
            x.cost=x.depth+misplacedTile(x)
        elif queue_function=='3':
            x.cost=x.depth+manhattanDistance(x)
        if [x.cost,x.puzzle] not in abc:
            nodes.append(x)
            abc.append([x.cost,x.puzzle])
    x=copy.deepcopy(node)
    x=left(x)
    if x is not None:
        x.depth=node.depth+1
        if queue_function=='1':
            x.cost=x.depth + 0
        if queue_function=='2':
            x.cost=x.depth+misplacedTile(x)
        elif queue_function=='3':
            x.cost=x.depth+manhattanDistance(x)
        if [x.cost,x.puzzle] not in abc:
            nodes.append(x)
            abc.append([x.cost,x.puzzle])
    x=copy.deepcopy(node)
    x=right(x)
    if x is not None:
        x.depth=node.depth+1
        if queue_function=='1':
            x.cost=x.depth + 0
        if queue_function=='2':
            x.cost=x.depth+misplacedTile(x)
        if queue_function=='3':
            x.cost=x.depth+manhattanDistance(x)
        if [x.cost,x.puzzle] not in abc:
            nodes.append(x)
            abc.append([x.cost,x.puzzle])
    nodes.sort(key=lambda x:(x.cost,x.depth))
    print ('\n[-] Exapnading at depth',str(nodes[0].depth),'\n')
    show_puzzle(nodes[0])
    return nodes
def show_puzzle(node: Node):
    for x in node.puzzle:
        for y in x: 
            if y == 0:
                print('_',end=' ')  
                continue  
            print(y,end=' ')
        print()
choice=int(input("Choose from following: \n1. Use Default Puzzle\n2. Enter Puzzle\nInput: "))
arr=[1,2] # array to manage the inputs 
abc=[] # queue to store visited states

if choice==arr[0]: # choose deafult puzzles 

    print("Default Puzzle selected")
    dif = input('Select the difficulty of the puzzle from a scale of 1 to 8\nInput: ')
    puzzle = default_puzzle[dif]
    # print selected puzzle 
    print ('Selected the puzzle: ')
    for x in puzzle:
        for y in x:
            if y == 0:
                print('_',end=' ')  
                continue  
            print(y,end=' ')
        print()

elif choice == arr[1]: 
     # taking input from user 
     print('Enter puzzle: \n(Use 0 instead of blank space "_")')
     puzzle = []
     n = int(input('Number of rows/columns: '))
     # converting into 2D List
     for i in range(n):
         t = list(map(int,input().split()))
         puzzle.append(t)

# if user inputs input other than 1 or 2 it asks for input again and again 
while(choice>len(arr)or choice<1):
    
    print('Invalid choice')
    
    choice=int(input("Choose from following: \n1. Use Default Puzzle\n2. Enter Puzzle\nInput: "))
    if choice==arr[0]:
        print("Default Puzzle selected")
        dif = input('Select the difficulty of the puzzle from a scale of 1 to 8\nInput: ')
        puzzle = default_puzzle[dif]
        # print selected puzzle 
        print ('Selected the puzzle: ')
        for x in puzzle:
            for y in x:
                if y == 0:
                    print('_',end=' ')  
                    continue  
                print(y,end=' ')
            print()
    
    elif choice == arr[1]: 
    # taking input from user 
        print('Enter puzzle: \n(Use 0 instead of blank space "_")')
        puzzle = []
        n = int(input('Number of rows/columns: '))
        # converting into 2D List
        for i in range(n):
            t = list(map(int,input().split()))
            puzzle.append(t)

# input for the choice of Algorithm 
algChoice =(input('Choose Algorithm from following: \n1. Uniform Cost Search \n2. A* with the misplacedTileplaced Tile heuristic \n3. A* with the Manhattan Distance heuristic\nInput: '))

root=Node(puzzle,0,0)

start=time.time() # https://stackoverflow.com/questions/7370801/how-do-i-measure-elapsed-time-in-python

result=generalSearch(root,algChoice)

end=time.time() # to measure the time elapsed for the algorithm 

print('Goal state reached!!')
for x in result.puzzle:
    for y in x: 
        if y == 0:
            print('_',end=' ')  
            continue  
        print(y,end=' ')
    print()
print('Solution found at depth', str(result.depth))
print('Algorithm took',str(round((end-start),5)),'seconds to complete')  # https://www.programiz.com/python-programming/methods/built-in/round

# Compiled this code in the ipython notebook 
# import plotly.express as px
# import pandas as pd
# B = ['UCS','AMT','AMD']
# A=[2.43705,0.02841,0.0261] # times taken for three algorithms of the puzzle with depth 4 
# # https://cmdlinetips.com/2018/01/how-to-create-pandas-dataframe-from-multiple-lists/
# data_tuples = list(zip(B,A))
# df=pd.DataFrame(data_tuples, columns=['Algorithm','Time'])
# # https://plotly.com/python/bar-charts/
# px.bar(df,x='Algorithm',y='Time', title="Time Compared for the puzzle with depth 4").show()