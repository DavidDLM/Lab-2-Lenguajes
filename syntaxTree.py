# Built with help from DL-Project-1
# Based on "Analizador Lexico" by Gerardo Mendez Alvarez

from machine import *
import copy


class SyntaxTree(object):
    # Create syntax tree from REGEX
    def __init__(this, operadores, er, direct=False):
        this.operadores = operadores
        this.er = er
        this.postfix = ""
        this.raiz = None
        this.direct = direct
        this.symbol = list(set([char for char in er
                                if char not in operadores
                                if char != '(' and char != ')']))
        this.normalRegex()
        this.infixToPostfix()
        this.postfixToTree()

        this.pos = 1

    # Identify operators and precedence
    def prec(char):
        if char == '|':
            return 1
        if char == '.':
            return 2
        if char == '+':
            return 3
        if char == '*':
            return 3
        if char == '?':
            return 3
        else:
            return 0

    # Concatenate with "."
    def normalRegex(this):
        temp = ""
        excepciones = ['|', '(']
        for i in range(len(this.er)):
            actual = 0
            next = 0
            temp += this.er[i]
            # Verify REGEX symbols
            try:
                if(this.er[i] in this.symbol and this.er[i+1] in this.symbol) \
                        or (this.er[i] not in excepciones and this.er[i + 1] in this.symbol + ['(']):
                    temp += '.'
            except:
                pass
        this.er = temp

    def getPrev(this, pos):
        try:
            prev = this.operadores[pos]
        except:
            prev = 0

        return prev

    # REGEX to postfix
    def infixToPostfix(this):
        operstack = Stack()
        #print("1. infix a postfix")
        for char in this.er:
            if char in this.symbol:
                this.postfix += char
                #print("char es symbol")
            elif char == '(':
                operstack.push(char)
                #print("char es parentesis (")
            elif char == ')':  # caso parentesis final o caso simplemente parentesis
                while operstack.peek() != '(':
                    this.postfix += operstack.pop()
                    if operstack.empty():
                        print("Fatal error in operators stack.")
                        exit()
                operstack.pop()
            else:
                while not operstack.empty():
                    top = operstack.peek()
                    primpos = this.getPrev(top)
                    simpos = this.getPrev(char)
                    if (primpos >= simpos):
                        this.postfix += operstack.pop()
                    else:
                        break
                operstack.push(char)
        while not operstack.empty():
            this.postfix += operstack.pop()
        # Refinar el postfix incluyendo epsilon en "?"
        refPostfix = ""
        for char in this.postfix:
            if char == '?':
                refPostfix += 'ε|'
                this.symbol.append('ε')
            else:
                refPostfix += char

        this.postfix = refPostfix

        print("Postfix: " + this.postfix)

    def postfixToTree(this):
        tstack = Stack()
        simb = ['*', '?', '+']  # Exclude kl, posC, parenthesis
        for char in this.postfix:
            if char in this.symbol:
                tstack.push(
                    Node(symbol=char, parent=None, prev=None, next=None))
            else:
                if char in simb:
                    if tstack.size() > 0:
                        # Order node logic
                        if this.direct and char == "+":
                            var = tstack.pop()
                            var2 = copy.deepcopy(var)
                            # Kleene
                            k = Node('*', parent=None, prev=None, next=var2)
                            # Concatenacion
                            c = Node('.', parent=None, prev=var, next=k)
                            var2.parent = k
                            k.parent = c
                            var.parent = c
                            tstack.push(c)
                        else:
                            next = tstack.pop()
                            temp = Node(char, parent=None,
                                        prev=None, next=next)
                            next.parent = temp
                            tstack.push(temp)
                    else:
                        print("Fatal error in tree nodes, empty stack.")
                else:
                    if tstack.size() > 1:
                        next = tstack.pop()
                        prev = tstack.pop()

                        temp = Node(char, parent=None, prev=prev, next=next, )
                        next.parent = temp
                        prev.parent = temp

                        tstack.push(temp)
                    else:
                        print("Fatal error in CONCAT / OR.")
                        exit()
        this.raiz = tstack.pop()  # Get tree root

    def positions(this, node, alcanzable=None, nodes=None, lleno=False):
        if not node:
            return
        if alcanzable is None:
            alcanzable = []
        if nodes is None:
            nodes = []
        this.positions(node.prev, alcanzable, nodes)
        this.positions(node.next, alcanzable, nodes)
        alcanzable.append(node.symbol)
        nodes.append(node)

        if node.symbol in this.symbol:
            # Define pos
            node.pos = this.pos
            this.pos += 1

            # Define nullable
            if node.symbol == 'ε':  # epsilon
                node.nullable = True
            else:
                node.nullable = False

            # Define first and last pos
            node.firstpos = [node.pos]
            node.lastpos = [node.pos]

        else:
            # If symbol is |, set nullable
            if node.symbol == '|':
                node.nullable = node.next.nullable or node.prev.nullable
                node.firstpos = list(
                    set(node.next.firstpos + node.prev.firstpos))
                node.lastpos = list(
                    set(node.next.lastpos + node.prev.lastpos))
            # If symbol is .
            elif node.symbol == '.':
                node.nullable = node.next.nullable and node.prev.nullable
                node.firstpos = list(set(node.next.firstpos + node.prev.firstpos)
                                     ) if node.prev.nullable else node.prev.firstpos
                node.lastpos = list(set(node.next.lastpos + node.prev.lastpos)
                                    ) if node.next.nullable else node.next.lastpos
            # If symbol is *
            elif node.symbol == '*':
                node.nullable = True
                node.firstpos = node.next.firstpos
                node.lastpos = node.next.lastpos
            else:
                pass
        if lleno:
            return nodes
        else:
            return alcanzable

    def treePrint(this, node):
        if node is not None:
            print(node.symbol)
            this.treePrint(node.prev)
            this.treePrint(node.next)
