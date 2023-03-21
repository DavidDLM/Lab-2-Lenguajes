from graphviz import Digraph
import copy
from collections import deque
EPSILON = 'ε'


class DFA:
    # constructor for DFA
    def __init__(this, startingState, finalState, states, symbols, transitions):
        this.startingState = startingState  # starting state
        this.finalState = finalState  # set of final states
        this.states = states  # set of all states
        this.symbols = symbols  # set of all input symbols
        this.transitions = transitions
        this.dfaTransitions = []  # dictionary of transitions
        this.dfaStates = []

    def recognize(this, states, symbol):
        dfa = []  # Reachable states
        for state in states:
            # Find all transitions for each symbol
            transition_symbol = [
                t[2] for t in this.transitions if t[0] == state and t[1] == symbol]
            dfa.extend(transition_symbol)
        return dfa  # Reachable states

    def case_epsilon(this, states):
        vertexStack = states.copy()
        nfa = states.copy()
        while vertexStack:
            currentState = vertexStack.pop()
            # Find all reachable states for epsilon
            epsilon_transition = [
                t[2] for t in this.transitions if t[0] == currentState and t[1] == EPSILON]
            for eps in epsilon_transition:
                if eps not in nfa:
                    nfa.append(eps)
                    vertexStack.append(eps)
        return nfa

    def compile(this):
        # Initialize the DFA with the starting state
        this.transitionsList = []
        this.splitTransitionsList = []
        this.finalStatesList = []
        vertexStack = []
        # Edge dictionary represents transitions to other states
        edgeDict = {}
        stateCount = 0
        this.states = []
        final_states_list = []
        startingState = None
        this.startingState_dfa = []
        this.finalState_dfa = []
        finalStates = None
        this.symbolList = []
        this.error = False

        startingState_closure = this.case_epsilon([this.startingState])
        this.dfaStates.append(startingState_closure)
        vertexStack = [startingState_closure]
        while vertexStack:
            current = vertexStack.pop(0)
            for symbol in this.symbols:
                # Find all reachable states for each input symbol
                reachable = (this.case_epsilon
                             (this.recognize(current, symbol)))
                if reachable not in this.dfaStates and symbol != EPSILON:
                    this.dfaStates.append(reachable)
                    this.dfaTransitions.append((this.dfaStates.index(
                        current), symbol, this.dfaStates.index(reachable)))
                    vertexStack.append(reachable)
                elif reachable in this.dfaStates and len(this.recognize(current, symbol)) != 0 and symbol != EPSILON:
                    this.dfaTransitions.append((this.dfaStates.index(
                        current), symbol, this.dfaStates.index(reachable)))

        dot = Digraph()
        # This will create a graph with nodes and edges,
        #  with labels indicating the direction of the edges.
        for i, state in enumerate(this.dfaStates):
            dot.node(str(i), label=str(chr(i+65)))
            if this.finalState in state:
                dot.node(str(i), shape='doublecircle')
        for transition in this.dfaTransitions:
            dot.edge(str(transition[0]), str(
                transition[2]), label=str(transition[1]))
        dot.render('DFA_Visualization', format='png', view=True)

        for i, state in enumerate(this.dfaStates):
            if i == 0:
                startingState = str(chr(i+65))
                this.startingState_dfa = i
            if this.finalState in state:
                final_states_list.append(str(chr(i+65)))
                this.finalState_dfa.append(i)
            this.states.append(i)

        with open('afd.txt', 'a', encoding="utf-8") as f:
            f.write("DFA")
            f.write("\n")
            f.write("Symbols: "+', '.join(this.symbols))
            f.write("\n")
            f.write("States:  " + str(this.dfaStates))
            f.write("\n")
            f.write("startingState: { " + str(startingState) + " }")
            f.write("\n")
            f.write(
                "finalState: { " + str(final_states_list) + " }")
            f.write("\n")
            f.write("transitionsList: " + str(this.dfaTransitions))
