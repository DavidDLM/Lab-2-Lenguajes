# Thompson function
# https://userpages.umbc.edu/~squire/cs451_l6.html
'''
The thompson function takes a regular expression as input
and returns the start state of the resulting NFA.
It uses a stack to keep track of sub-expressions,
and constructs the NFA incrementally as it processes each
symbolacter of the input string

'''

from re import S
import pandas as pd
from graphviz import Digraph
from machine import *
import matplotlib.pyplot as plt

EPSILON = 'ε'


class Thompson():
    def __init__(this, regex):
        this.transitionsList = []
        this.splitTransitionsList = []
        this.regex = regex
        this.finalStatesList = []
        vertexStack = []
        # Edge dictionary represents transitions to other states
        edgeDict = {}
        stateCount = 0
        this.states = []
        this.states_list = []
        this.startingState = None
        this.finalState = None
        this.symbolList = []
        this.error = False

    def compile(this):
        this.case_concurrence()
        symbolList = []
        regex = this.regex
        for char in regex:
            if this.item(char):
                if char not in symbolList:
                    symbolList.append(char)

        this.symbolList = sorted(symbolList)

        vertexStack = []
        start = 0
        end = 1

        counter = -1
        automata_counter_1 = 0
        automata_counter_2 = 0

        # Thompson algorithm
        for symbol in regex:
            # Left parenthesis management
            if symbol == "(":
                vertexStack.append(startingState)
                startingState = None
                finalState = None
            # Right (end) parenthesis management
            elif symbol == ")":
                finalState = vertexStack.pop()
                if not vertexStack:
                    startingState = None
                else:
                    startingState = vertexStack[-1]
            # If kleene
            # Kleene star, 4 nodes, 4 transitions
            # From q1 to qfinal, Epsilon
            elif symbol == '*':
                try:
                    '''
                    # Kleene star guide/template:

                    new_start = State(stateCount)
                    new_end = State(stateCount)
                    end_state.add_transition(EPSILON, start_state)
                    end_state.add_transition(EPSILON, new_end)
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, new_end)
                    start_state = new_start
                    end_state = new_end

                    '''
                    # Save states in variables
                    # Add transitions (Kleene Star: 4 transitions)
                    # Also add transitions to transition list
                    item1, item2 = vertexStack.pop()
                    counter = counter+1
                    automata_counter_1 = counter
                    if automata_counter_1 not in this.states:
                        this.states.append(automata_counter_1)
                    counter = counter+1
                    automata_counter_2 = counter
                    if automata_counter_2 not in this.states:
                        this.states.append(automata_counter_2)
                    this.finalStatesList.append({})
                    this.finalStatesList.append({})
                    vertexStack.append(
                        [automata_counter_1, automata_counter_2])
                    this.finalStatesList[item2]['ε'] = (
                        item1, automata_counter_2)
                    this.finalStatesList[automata_counter_1]['ε'] = (
                        item1, automata_counter_2)
                    if start == item1:
                        start = automata_counter_1
                    if end == item2:
                        end = automata_counter_2
                    this.splitTransitionsList.append([item2, EPSILON, item1])
                    this.splitTransitionsList.append(
                        [item2, EPSILON, automata_counter_2])
                    this.splitTransitionsList.append(
                        [automata_counter_1, EPSILON, item1])
                    this.splitTransitionsList.append(
                        [automata_counter_1, EPSILON, automata_counter_2])
                except:
                    this.error = True
                    print("\nKleene error.")
            # If OR
            elif symbol == "|":
                try:
                    '''
                    # OR guide/template:

                    new_start = State()
                    new_end = State()
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, end_state)
                    start_state = new_start
                    end_state = new_end

                    '''
                    # Save states in variables
                    # Add transitions (OR: 4 transitions)
                    # Also add transitions to transition list
                    counter = counter+1
                    automata_counter_1 = counter
                    if automata_counter_1 not in this.states:
                        this.states.append(automata_counter_1)
                    counter = counter+1
                    automata_counter_2 = counter
                    if automata_counter_2 not in this.states:
                        this.states.append(automata_counter_2)
                    this.finalStatesList.append({})
                    this.finalStatesList.append({})

                    item11, item12 = vertexStack.pop()
                    item21, item22 = vertexStack.pop()
                    vertexStack.append(
                        [automata_counter_1, automata_counter_2])
                    this.finalStatesList[automata_counter_1]['ε'] = (
                        item21, item11)
                    this.finalStatesList[item12]['ε'] = automata_counter_2
                    this.finalStatesList[item22]['ε'] = automata_counter_2
                    if start == item11 or start == item21:
                        start = automata_counter_1
                    if end == item22 or end == item12:
                        end = automata_counter_2
                    this.splitTransitionsList.append(
                        [automata_counter_1, EPSILON, item21])
                    this.splitTransitionsList.append(
                        [automata_counter_1, EPSILON, item11])
                    this.splitTransitionsList.append(
                        [item12, EPSILON, automata_counter_2])
                    this.splitTransitionsList.append(
                        [item22, EPSILON, automata_counter_2])
                except:
                    this.error = True
                    print("\nOR error.")

            # if Concatenation
            elif symbol == '.':
                try:
                    '''
                    # Concatenation guide/template:

                    new_start = State()
                    new_end = State()
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, end_state)
                    start_state = new_start
                    end_state = new_end

                    ---------------------------------

                    e2 = stack.pop()
                    e1 = stack.pop()
                    e1.accept = False
                    e1.edges[None] = [e2]
                    stack.append(e1)
                    stack.append(e2)s

                    '''
                    # Save states in variables
                    item11, item12 = vertexStack.pop()
                    item21, item22 = vertexStack.pop()
                    vertexStack.append([item21, item12])
                    this.finalStatesList[item22]['ε'] = item11
                    if start == item11:
                        start = item21
                    if end == item22:
                        end = item12
                    this.splitTransitionsList.append([item22, EPSILON, item11])

                except:
                    this.error = True
                    print(
                        "\nConcatenation error.")
            # if positive
            elif symbol == '+':
                try:
                    '''
                    # Union guide/template:

                    new_start = State()
                    new_end = State()
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, end_state)
                    start_state = new_start
                    end_state = new_end

                    '''
                    # Save states in variables
                    # Add transitions (UNION: 3 transitions)
                    # Add transition to transition list
                    item1, item2 = vertexStack.pop()
                    counter = counter+1
                    automata_counter_1 = counter
                    if automata_counter_1 not in this.states:
                        this.states.append(automata_counter_1)
                    counter = counter+1
                    automata_counter_2 = counter
                    if automata_counter_2 not in this.states:
                        this.states.append(automata_counter_2)
                    this.finalStatesList.append({})
                    this.finalStatesList.append({})
                    vertexStack.append(
                        [automata_counter_1, automata_counter_2])
                    this.finalStatesList[item2]['ε'] = (
                        item1, automata_counter_2)
                    if start == item1:
                        start = automata_counter_1
                    if end == item2:
                        end = automata_counter_2
                    this.splitTransitionsList.append([item2, EPSILON, item1])
                    this.splitTransitionsList.append(
                        [item2, EPSILON, automata_counter_2])
                    this.splitTransitionsList.append(
                        [automata_counter_1, EPSILON, item1])
                except:
                    this.error = True
                    print("\n+ error.")
            # If concurrence
            elif symbol == "?":
                try:
                    '''
                    # Concurrence guide/template:

                    new_start = State(stateCount)
                    new_end = State(stateCount)
                    end_state.add_transition(EPSILON, start_state)
                    end_state.add_transition(EPSILON, new_end)
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, new_end)
                    start_state = new_start
                    end_state = new_end

                    '''
                    # Save states in variables
                    # Add transitions (CONCURRENCE: 3 transitions)
                    # Add transition to transition list
                    counter = counter+1
                    automata_counter_1 = counter
                    if automata_counter_1 not in this.states:
                        this.states.append(automata_counter_1)
                    counter = counter+1
                    automata_counter_2 = counter
                    if automata_counter_2 not in this.states:
                        this.states.append(automata_counter_2)
                    this.finalStatesList.append({})
                    this.finalStatesList.append({})

                    item11, item12 = vertexStack.pop()
                    item21, item22 = vertexStack.pop()
                    vertexStack.append(
                        [automata_counter_1, automata_counter_2])
                    this.finalStatesList[automata_counter_1]['ε'] = (
                        item21, item11)
                    this.finalStatesList[item12]['ε'] = automata_counter_2
                    this.finalStatesList[item22]['ε'] = automata_counter_2
                    if start == item11 or start == item21:
                        start = automata_counter_1
                    if end == item22 or end == item12:
                        end = automata_counter_2
                    this.splitTransitionsList.append(
                        [automata_counter_1, EPSILON, item21])
                    this.splitTransitionsList.append(
                        [automata_counter_1, EPSILON, item11])
                    this.splitTransitionsList.append(
                        [item12, EPSILON, automata_counter_2])
                    this.splitTransitionsList.append(
                        [item22, EPSILON, automata_counter_2])
                except:
                    error = True
                    print("\nCONCURRENCE error.")
            else:
                if symbol in symbolList:
                    counter = counter+1
                    automata_counter_1 = counter
                    if automata_counter_1 not in this.states:
                        this.states.append(automata_counter_1)
                    counter = counter+1
                    automata_counter_2 = counter
                    if automata_counter_2 not in this.states:
                        this.states.append(automata_counter_2)
                    this.finalStatesList.append({})
                    this.finalStatesList.append({})
                    vertexStack.append(
                        [automata_counter_1, automata_counter_2])
                    this.finalStatesList[automata_counter_1][symbol] = automata_counter_2
                    this.splitTransitionsList.append(
                        [automata_counter_1, symbol, automata_counter_2])

        this.startingState = start
        this.finalState = end
        df = pd.DataFrame(this.finalStatesList)
        string_afn = df.to_string()
        '''
        To convert a list to a dictionary using the same values,
        you can use the dict.fromkeys() method. To convert two lists
        into one dictionary, you can use the Python zip() function.
        The dictionary comprehension lets you create a new dictionary
        based on the values of a list.

        '''
        for i in range(len(this.splitTransitionsList)):
            this.transitionsList.append(
                "(" + str(this.splitTransitionsList[i][0]) + " - " + str(this.splitTransitionsList[i][1]) + " - " + str(this.splitTransitionsList[i][2]) + ")")
        this.transitionsList = ', '.join(this.transitionsList)

        for i in range(len(this.states)):
            if i == len(this.states)-1:
                finalState = i
            this.states_list.append(str(this.states[i]))
        this.states_list = ", ".join(this.states_list)

        if this.error == False:
            with open('nfa.txt', 'a', encoding="utf-8") as f:
                f.write("NFA")
                f.write("\n")
                f.write("Symbols: "+', '.join(symbolList))
                f.write("\n")
                f.write("States:  " + str(this.states_list))
                f.write("\n")
                f.write("Q0: { " + str(this.startingState) + " }")
                f.write("\n")
                f.write("Qf: { " + str(this.finalState) + " }")
                f.write("\n")
                f.write("transitionsList: " + str(this.transitionsList))
                f.write("\n")
                f.write(string_afn)
            this.paintGraph('NFA_Visualization')
        else:
            print("\nInvalid regex.")

    def case_epsilon(this, states):
        result = states.copy()
        vertexStack = states.copy()
        while vertexStack:
            current = vertexStack.pop()
            epsilon_transitionsList = [
                t[2] for t in this.splitTransitionsList if t[0] == current and t[1] == EPSILON]
            for e in epsilon_transitionsList:
                if e not in result:
                    result.append(e)
                    vertexStack.append(e)
        return result

    def char_string(this, charString):
        current_states = this.case_epsilon([this.startingState])
        final_states = []
        for symbol in charString:
            newStates = []
            for state in current_states:
                for transition in this.splitTransitionsList:
                    if state == transition[0] and symbol == transition[1]:
                        newStates.append(transition[2])
            if not newStates:
                return False
            current_states = this.case_epsilon(newStates)
        final_states = this.case_epsilon(current_states)
        return this.finalState in final_states

    def paintGraph(this, name):
        # This will create a graph with nodes and edges,
        #  with labels indicating the direction of the edges.
        dot = Digraph()
        for i in range(len(this.states)):
            if this.states[i] == this.finalState:
                dot.node(str(this.states[i]), shape="doublecircle")
            else:
                dot.node(str(this.states[i]), shape="circle")
        for transition in this.splitTransitionsList:
            if transition[1] == EPSILON:
                dot.edge(str(transition[0]), str(transition[2]), label=EPSILON)
            else:
                dot.edge(str(transition[0]), str(
                    transition[2]), label=transition[1])
        dot.render(name, format='png', view=True)

    def item(this, character):
        # Recognize character
        if(character.isalpha() or character.isnumeric() or character == EPSILON):
            return True
        else:
            return False

    def case_concurrence(this):
        # Case concurrence
        # Replace concurrence with epsilon
        this.regex = this.regex.replace('?', 'ε?')
