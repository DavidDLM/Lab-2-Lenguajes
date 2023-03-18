# https://leetcode.com/problems/basic-calculator/solutions/1662949/python-actually-working-shunting-yard-that-passes-all-edge-cases/
EPSILON = 'ε'
precedence = {'|': 1, '.': 1, '?': 2, '*': 2, '+': 2}


class shunting_yard:
    def __init__(this, length):
        this.top = -1
        this.length = length
        this.array = []
        # Operator precedence dictionary
        this.precedence = {'|': 1, '.': 1, '?': 2, '*': 2, '+': 2}
        this.output = []
        this.res = ""

    # Add concat
    def addConcatenation(this, regex):
        symbols = [".", "|", "?", "*", "+", "(", ")"]
        length = len(regex)
        new_regex = []
        for i in range(length-1):
            new_regex.append(regex[i])
            if regex[i] not in symbols:
                if regex[i+1] not in symbols or regex[i+1] == '(':
                    new_regex += "."
            if regex[i] == ")" and regex[i+1] == "(":
                new_regex += "."
            if regex[i] == "*" and regex[i+1] == "(":
                new_regex += "."
            if regex[i] == "?" and regex[i+1] == "(":
                new_regex += "."
            if regex[i] == ")" and regex[i+1] not in symbols:
                new_regex += "."
            if regex[i] == "*" and regex[i+1] not in symbols:
                new_regex += "."
            if regex[i] == "+" and regex[i+1] not in symbols:
                new_regex += "."
            if regex[i] == "?" and regex[i+1] not in symbols:
                new_regex += "."
        new_regex += regex[length-1]

        return "".join(new_regex)

    # Element push
    def push(this, item):
        this.top += 1
        this.array.append(item)
     # Element pop

    def pop(this):
        if not this.is_empty():
            this.top -= 1
            return this.array.pop()
        else:
            return "$"
    # Stack operations

    def peek(this):
        try:
            return this.array[-1]
        except:
            pass

    def is_empty(this):
        return True if this.top == -1 else False

    # Check symbols
    def operando(this, caracter):
        if(caracter.isalnum() or caracter == "ε"):
            return True
        else:
            return False

    # Check precedence
    def revision(this, item):
        try:
            a = this.precedence[item]
            b = this.precedence[this.peek()]
            return True if a <= b else False
        except KeyError:
            return False

    # Check parenthesis
    def parenthesis(this, exp):
        count = 0
        for char in exp:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count < 0:
                    return False
        return count == 0

    def shunting_yard(this, exp):
        this.ver = this.parenthesis(exp)
        if this.ver == True:
            exp = this.addConcatenation(exp)
            for i in exp:
                if this.operando(i):
                    if this.peek() == "*" or this.peek() == "+" or this.peek() == "?":
                        this.output.append(this.pop())
                    this.output.append(i)
                elif i == '(':
                    this.push(i)
                elif i == ')':
                    while((not this.is_empty()) and this.peek() != '('):
                        a = this.pop()
                        this.output.append(a)
                    if (not this.is_empty() and this.peek() != '('):
                        return -1
                    else:
                        this.pop()
                else:
                    while(not this.is_empty() and this.revision(i)):
                        this.output.append(this.pop())
                    this.push(i)
            while not this.is_empty():
                this.output.append(this.pop())
            this.res = "".join(this.output)
        else:
            print("\nParenthesis fatal error. Uneven parenthesis.")
