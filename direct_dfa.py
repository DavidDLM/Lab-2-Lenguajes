import os  # The functions OS module provides allows us to operate on underlying Operating System tasks
import uuid
import shortuuid  # shortuuid is a simple python library that generates concise, unambiguous, URL-safe UUIDs
import graphviz
import tempfile
from machine import *
from syntaxTree import SyntaxTree

output = os.environ["PATH"]
output += os.pathsep + 'C:\Program Files\Graphviz\bin'
# Set alphabet for states
shortuuid.set_alphabet("ABC")
EPSILON = 'ε'

# Create an automata with its elements
# https://stackoverflow.com/questions/35272592/how-are-finite-automata-implemented-in-code


class DFANode:
    def __init__(this, val):
        this.val = val
        this.links = []

    def add_link(this, link):
        this.links.append(link)

    def __str__(this):
        node = "(%s):\n" % this.val
        for link in this.links:
            node += "\t" + link + "\n"
        return node

    def __add__(this, other):
        return str(this) + other

    def __radd__(this, other):
        return other + str(this)

    def equals(this, node):
        ok = (this.val == node.val)
        if len(this.links) == len(node.links):
            for i in range(len(this.links)):
                ok = ok and (this.links[i] == node.links[i])
            return ok
        else:
            return False


# https://stackoverflow.com/questions/35272592/how-are-finite-automata-implemented-in-code
class Automata(object):

    def __init__(this, symbols, nodes, tfunc, initial_node, terminal_node):
        this.nodes = nodes
        this.symbol = symbols
        this.transition_function = tfunc
        this.initial_node = initial_node
        this.terminal_nodes = terminal_node

    def graphAutomata(this, mapping=None):
        # Rankdir: Direction to draw directed graphs (one rank at a time)
        # LR: left to right
        draw = graphviz.Digraph(graph_attr={'rankdir': 'LR'})
        for x in this.nodes:
            x = x if not mapping else mapping[tuple(x)]
            # Identify final nodes and not-final nodes
            if x not in this.terminal_nodes:
                draw.attr('node', shape='circle')
                draw.node(x)
            else:
                draw.attr('node', shape='doublecircle')
                draw.node(x)

        draw.attr('node', shape='none')
        draw.node('')
        draw.edge('', this.initial_node)

        for k, v in this.transition_function.items():
            if isinstance(v, str):
                draw.edge(k[0], v, label=(k[1]))
            else:
                for val in v:
                    draw.edge(k[0], val, label=(k[1]))
        # TEMPFILE direct visualization (temp)
        # User is responsible for deleting files
        draw.view(tempfile.mktemp('.gv'), cleanup=True, )


# Create a DFA instance with automata
# Contains starting node, final node, symbols, syntax tree, etc.
class DirectDFA(Automata):
    def __init__(this, syntaxTree=None, symbols=None, nodes=[], tfunc={}, initial_node=None, terminal_node=[], direct=False, circs=None):
        this.syntaxTree = syntaxTree
        this.circs = circs
        this.dfamap = None
        # Remove epsilon
        syntaxTree and 'ε' in syntaxTree.symbol and syntaxTree.symbol.remove(
            'ε')
        Automata.__init__(
            this,
            symbols=syntaxTree.symbol,
            nodes=nodes,
            tfunc=tfunc,
            initial_node=initial_node,
            terminal_node=terminal_node
        )

    def get_next_node(this, current_node, etiquette):
        for link in current_node.links:
            if link.etiquette == etiquette:
                return link.to_node
        return None

    def accepts(this, string):
        circ = this.initial_node
        for character in string:
            circ = this.get_next_node(circ, character)
        return this.terminal_nodes.equals(circ)

    def __str__(this):
        automata = "Initial node: %s\nTerminal node: %s\n" % (
            this.initial_node.val, this.terminal_nodes.val)
        for circ in this.circ:
            automata += circ
        return automata

    def __add__(this, other):
        return str(this) + other

    def __radd__(this, other):
        return other + str(this)

    # Define different cases, for example case . o case *
    # Note: with match -> case didnt work, so use ifs

    def nextPos(this):
        this.nextPos = {}
        for circ in this.circs:
            if circ.pos:
                this.nextPos[circ.pos] = []
        for circ in this.circs:
            if circ.symbol == '.':
                for i in circ.prev.lastpos:
                    this.nextPos[i] += circ.next.firstpos
            if circ.symbol == '*':
                for i in circ.lastpos:
                    this.nextPos[i] += circ.firstpos

    # buildGraph
    def buildGraph(this):
        # Call nextPos
        this.nextPos()
        # Print nextpos from AFD
        print("NextPos: ")
        print(this.nextPos)
        # variables
        finPos = 0
        trans_func = {}
        smap = {}
        DUNodes = [this.syntaxTree.raiz.firstpos]
        DMNodes = []
        for circ in this.circs:
            if circ.symbol == '#':
                # Put "#" as last symbol
                finPos = circ.pos
        while len(DUNodes) > 0:
            x = DUNodes.pop(0)
            DMNodes.append(x)
            for s in this.symbol:
                x1 = []
                for node in this.circs:
                    if node.symbol == s and node.pos in x:
                        x1 += this.nextPos[node.pos]
                        x1 = list(set(x1))

                if len(x1) > 0:
                    if x1 not in DUNodes and x1 not in DMNodes:
                        DUNodes.append(x1)

                    try:
                        smap[tuple(x)]
                    except:
                        smap[tuple(x)] = shortuuid.encode(
                            uuid.uuid4())[:2]

                    try:
                        smap[tuple(x1)]
                    except:
                        smap[tuple(x1)] = shortuuid.encode(
                            uuid.uuid4())[:2]

                    trans_func[(smap[tuple(x)], s)
                               ] = smap[tuple(x1)]

        for node in DMNodes:
            if finPos in node:
                this.terminal_nodes.append(smap[tuple(node)])

        this.initial_node = smap[tuple(DMNodes[0])]
        this.nodes = DMNodes
        this.transition_function = trans_func
        this.dfamap = smap
