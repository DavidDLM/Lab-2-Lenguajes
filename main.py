import postfix
from direct_dfa import DFA
from syntaxTree import SyntaxTree
from thompson import Thompson
from postfix import *
from nfa_dfa import NFAtoDFA

# Direct DFA
# ---------------------------------------------------------
# Operators
operators = {'|': 1, '.': 2, '+': 3, '*': 3, '?': 3}
regex = input("Regular expression: ")
canonicalER = '(' + regex + ')' + '#'
tree = SyntaxTree(operators, canonicalER, direct=True)
pts = tree.positions(tree.raiz, lleno=True)
# DFA Ops
dfa = DFA(syntaxTree=tree, direct=True, circs=pts)
# Create DFA in memory
dfa.buildGraph()
# Show DFA
dfa.graphAutomata(mapping=dfa.dfamap)
# ---------------------------------------------------------

# NFA to DFA
# ---------------------------------------------------------
ptf = postfix.shunting_yard(regex)
# Convert postfix to NFA
print("Postfix value: " + ptf)
# Create new NFA
new_nfa = Thompson(ptf)
new_nfa.compile()
# Create new DFA
new_dfa = NFAtoDFA(new_nfa.startingState, new_nfa.finalState,
                   new_nfa.states, new_nfa.symbolList, new_nfa.splitTransitionsList)
new_dfa.compile()
# NFA simulation
char_string = input("\nString to be evaluated in NFA:\n")
accept_string = new_nfa.char_string(char_string)
if accept_string:
    print(f"\nString '{char_string}' was accepted.")
else:
    print(f"\nString '{char_string}' wasnt accepted.")
# ---------------------------------------------------------
