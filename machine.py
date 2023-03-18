from queue import LifoQueue  # For stack operations


# Machine class
class Machine:
    def __init__(this, initialState, finalState):
        this.initialState = initialState
        this.finalState = finalState

    def getFinalMachineState(this):
        return this.finalState

    def getInitialMachineState(this):
        return this.initialState

    def display():
        return


# State class
class State:

    def __init__(this, state_id):
        this.state_id = state_id

    def __repr__(this):
        return str(this.state_id)


# Transitions class
class Transitions:
    def __init__(this, initialState, finalState, symbol):
        this.initialState = initialState
        this.finalState = finalState
        this.symbol = symbol

    def getInitialTransitionState(this):
        return this.initialState

    def setInitialTransitionState(this, initialState):
        this.initialState = initialState

    def getFinalTransitionState(this):
        return this.finalState

    def setFinalTransitionState(this, finalState):
        this.finalState = finalState

    def getTransitionSymbol(this):
        return this.symbol


# Clase Node based in a node from Linked List
# https://www.tutorialspoint.com/python_data_structure/python_linked_lists.htm
class Node(object):
    # Node class with parents, right node, left node, symbols
    def __init__(this, symbol, parent, prev, next):
        this.symbol = symbol
        this.parent = parent
        this.prev = prev
        this.next = next
        this.nullable = False
        this.firstpos = []
        this.lastpos = []
        this.followpos = []
        this.pos = None


# Stack class with stack functions
# Import LastInFirstOut
# https://codefather.tech/blog/create-stack-python/#:~:text=To%20create%20a%20stack%20in%20Python%20you%20can%20use%20a,the%20top%20of%20the%20stack.
class Stack:
    def __init__(this):
        this.elements = LifoQueue()

    def push(this, data):
        this.elements.put(data)

    def pop(this):
        return this.elements.get()

    def size(this):
        return this.elements.qsize()

    def empty(this):
        return this.elements.empty()

    def peek(this):
        peek = this.pop()
        this.elements.put(peek)
        return peek
