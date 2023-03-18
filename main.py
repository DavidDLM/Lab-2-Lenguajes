import postfix
from direct_dfa import DFA
from syntaxTree import SyntaxTree
from thompson import Thompson
from postfix import shunting_yard

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
# -------------------PostifixToNFA--------------------------------------

# NFA to DFA
# ---------------------------------------------------------
ptf = shunting_yard(len(regex))
# Convert postfix to NFA
ptf.shunting_yard(regex)
postfixExp = ptf.res
print("Postfix value: " + postfixExp)
# Create new NFA
new_nfa = Thompson(postfixExp)
new_nfa.compile()
# NFA simulation
char_string = input("\nString to be evaluated in NFA:\n-> ")
accept_string = new_nfa.char_string(char_string)
if accept_string:
    print(f"\nString '{char_string}' was accepted.")
else:
    print(f"\nString '{char_string}' wasnt accepted.")
# ---------------------------------------------------------
