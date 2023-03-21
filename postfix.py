# https://leetcode.com/problems/basic-calculator/solutions/1662949/python-actually-working-shunting-yard-that-passes-all-edge-cases/

EPSILON = 'ε'
# Operator precedence dictionary
precedence = {'(': 1, '|': 2, '.': 3, '?': 4, '*': 4, '+': 4, '^': 5}


# Shunting Yard algorithm
def shunting_yard(expression):
    postfix = ''
    tempStack = []
    formatted_regex = clean_regex(expression)
    for char in formatted_regex:
        if char == '(':
            tempStack.append(char)
        elif char == ')':
            while tempStack[-1] != '(':
                postfix += tempStack.pop()
            tempStack.pop()
        # Operator
        else:
            while len(tempStack) > 0:
                top_char = tempStack[-1]
                current_char_precedence = get_precedence(char)
                top_char_precedence = get_precedence(top_char)
                if top_char_precedence >= current_char_precedence:
                    postfix += tempStack.pop()
                else:
                    break
            tempStack.append(char)
    while tempStack:
        # Processing the postfix
        postfix += tempStack.pop()
    return postfix


# We need to explicitly include '.' between concats
# This is needed to create valid postfix expressions for shunting yard
def clean_regex(expression):
    ans = ''
    # Both of the ones below can be extended to support many operation types (*/** etc)
    ops = set(['?', '+', '|', '*', '^'])
    bOps = set(['|', '^'])
    for i in range(len(expression)):
        char1 = expression[i]
        if i + 1 < len(expression):
            char2 = expression[i + 1]
            ans += char1
            if char1 != '(' and char2 != ')' and char2 not in ops and char1 not in bOps:
                ans += '.'
    ans += expression[-1]
    return ans


"""
    this is needed to create valid postfix expressions for shunting yard
    eg: 1 - (-2) creates a postfix of 1 2 - - which is invalid
    instead we convert to 1 0 2 - -
"""


def get_precedence(char):
    return precedence.get(char, 6)
