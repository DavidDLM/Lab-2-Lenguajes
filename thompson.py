from re import S
import pandas as pd
from graphviz import Digraph


class PostifixToNFA():
    def __init__(this, regex):
        this.regex = regex
        this.states = []
        this.states_list = []
        this.e0 = None
        this.ef = None
        this.transitions = []
        this.transitions_splited = []
        this.simbolos = []
        this.afn_final = []
        this.error = False

    def paintGraph(this, nombre):
        dot = Digraph()
        for i in range(len(this.states)):
            if this.states[i] == this.ef:
                dot.node(str(this.states[i]), shape="doublecircle")
            else:
                dot.node(str(this.states[i]), shape="circle")
        for transicion in this.transitions_splited:
            if transicion[1] == "ε":
                dot.edge(str(transicion[0]), str(transicion[2]), label="ε")
            else:
                dot.edge(str(transicion[0]), str(
                    transicion[2]), label=transicion[1])
        dot.render(nombre, format='png', view=True)

    def item(this, caracter):
        if(caracter.isalpha() or caracter.isnumeric() or caracter == "ε"):
            return True
        else:
            return False

    def case_concurrence(this):
        this.regex = this.regex.replace('?', 'ε?')

    def conversion(this):
        print("\nregex: ", this.regex)
        this.case_concurrence()
        simbolos = []
        regex = this.regex
        for i in regex:
            if this.item(i):
                if i not in simbolos:
                    simbolos.append(i)

        this.simbolos = sorted(simbolos)

        stack = []
        start = 0
        end = 1

        counter = -1
        c1 = 0
        c2 = 0

        # Thompson algorithm
        for i in regex:
            # If symbol
            if i in simbolos:
                counter = counter+1
                c1 = counter
                if c1 not in this.states:
                    this.states.append(c1)
                counter = counter+1
                c2 = counter
                if c2 not in this.states:
                    this.states.append(c2)
                this.afn_final.append({})
                this.afn_final.append({})
                stack.append([c1, c2])
                this.afn_final[c1][i] = c2
                this.transitions_splited.append([c1, i, c2])
            # If kleene
            elif i == '*':
                try:
                    r1, r2 = stack.pop()
                    counter = counter+1
                    c1 = counter
                    if c1 not in this.states:
                        this.states.append(c1)
                    counter = counter+1
                    c2 = counter
                    if c2 not in this.states:
                        this.states.append(c2)
                    this.afn_final.append({})
                    this.afn_final.append({})
                    stack.append([c1, c2])
                    this.afn_final[r2]['ε'] = (r1, c2)
                    this.afn_final[c1]['ε'] = (r1, c2)
                    if start == r1:
                        start = c1
                    if end == r2:
                        end = c2
                    this.transitions_splited.append([r2, "ε", r1])
                    this.transitions_splited.append([r2, "ε", c2])
                    this.transitions_splited.append([c1, "ε", r1])
                    this.transitions_splited.append([c1, "ε", c2])
                except:
                    this.error = True
                    print("\nKleene error.")
            # If +
            elif i == '+':
                try:
                    r1, r2 = stack.pop()
                    counter = counter+1
                    c1 = counter
                    if c1 not in this.states:
                        this.states.append(c1)
                    counter = counter+1
                    c2 = counter
                    if c2 not in this.states:
                        this.states.append(c2)
                    this.afn_final.append({})
                    this.afn_final.append({})
                    stack.append([c1, c2])
                    this.afn_final[r2]['ε'] = (r1, c2)
                    if start == r1:
                        start = c1
                    if end == r2:
                        end = c2
                    this.transitions_splited.append([r2, "ε", r1])
                    this.transitions_splited.append([r2, "ε", c2])
                    this.transitions_splited.append([c1, "ε", r1])
                except:
                    this.error = True
                    print("\n+ error.")

            # if Concatenation
            elif i == '.':
                try:
                    r11, r12 = stack.pop()
                    r21, r22 = stack.pop()
                    stack.append([r21, r12])
                    this.afn_final[r22]['ε'] = r11
                    if start == r11:
                        start = r21
                    if end == r22:
                        end = r12
                    this.transitions_splited.append([r22, "ε", r11])

                except:
                    this.error = True
                    print(
                        "\nConcatenation error.")
            # if Or
            elif i == "|":
                try:
                    counter = counter+1
                    c1 = counter
                    if c1 not in this.states:
                        this.states.append(c1)
                    counter = counter+1
                    c2 = counter
                    if c2 not in this.states:
                        this.states.append(c2)
                    this.afn_final.append({})
                    this.afn_final.append({})

                    r11, r12 = stack.pop()
                    r21, r22 = stack.pop()
                    stack.append([c1, c2])
                    this.afn_final[c1]['ε'] = (r21, r11)
                    this.afn_final[r12]['ε'] = c2
                    this.afn_final[r22]['ε'] = c2
                    if start == r11 or start == r21:
                        start = c1
                    if end == r22 or end == r12:
                        end = c2
                    this.transitions_splited.append([c1, "ε", r21])
                    this.transitions_splited.append([c1, "ε", r11])
                    this.transitions_splited.append([r12, "ε", c2])
                    this.transitions_splited.append([r22, "ε", c2])
                except:
                    this.error = True
                    print("\nOR error.")
            # If concurrence
            elif i == "?":
                counter = counter+1
                c1 = counter
                if c1 not in this.states:
                    this.states.append(c1)
                counter = counter+1
                c2 = counter
                if c2 not in this.states:
                    this.states.append(c2)
                this.afn_final.append({})
                this.afn_final.append({})

                r11, r12 = stack.pop()
                r21, r22 = stack.pop()
                stack.append([c1, c2])
                this.afn_final[c1]['ε'] = (r21, r11)
                this.afn_final[r12]['ε'] = c2
                this.afn_final[r22]['ε'] = c2
                if start == r11 or start == r21:
                    start = c1
                if end == r22 or end == r12:
                    end = c2
                this.transitions_splited.append([c1, "ε", r21])
                this.transitions_splited.append([c1, "ε", r11])
                this.transitions_splited.append([r12, "ε", c2])
                this.transitions_splited.append([r22, "ε", c2])
        this.e0 = start
        this.ef = end
        df = pd.DataFrame(this.afn_final)
        string_afn = df.to_string()
        for i in range(len(this.transitions_splited)):
            this.transitions.append(
                "(" + str(this.transitions_splited[i][0]) + " - " + str(this.transitions_splited[i][1]) + " - " + str(this.transitions_splited[i][2]) + ")")
        this.transitions = ', '.join(this.transitions)

        for i in range(len(this.states)):
            if i == len(this.states)-1:
                ef = i
            this.states_list.append(str(this.states[i]))
        this.states_list = ", ".join(this.states_list)

        if this.error == False:

            with open('nfa.txt', 'a', encoding="utf-8") as f:
                f.write("NFA")
                f.write("\n")
                f.write("Symbols: "+', '.join(simbolos))
                f.write("\n")
                f.write("States:  " + str(this.states_list))
                f.write("\n")
                f.write("Q0: { " + str(this.e0) + " }")
                f.write("\n")
                f.write("Qf: { " + str(this.ef) + " }")
                f.write("\n")
                f.write("Transitions: " + str(this.transitions))
                f.write("\n")
                f.write(string_afn)
            this.paintGraph('NFA_Visualization')
        else:
            print("\nInvalid regex.")

    def case_epsilon(this, states):
        resultado = states.copy()
        pila = states.copy()
        while pila:
            actual = pila.pop()
            epsilon_transitions = [
                t[2] for t in this.transitions_splited if t[0] == actual and t[1] == "ε"]
            for e in epsilon_transitions:
                if e not in resultado:
                    resultado.append(e)
                    pila.append(e)
        return resultado

    def char_string(this, cadena):
        current_states = this.case_epsilon([this.e0])
        final_states = []
        for simbolo in cadena:
            nuevos_states = []
            for estado in current_states:
                for transicion in this.transitions_splited:
                    if estado == transicion[0] and simbolo == transicion[1]:
                        nuevos_states.append(transicion[2])
            if not nuevos_states:
                return False
            current_states = this.case_epsilon(nuevos_states)
        final_states = this.case_epsilon(current_states)
        return this.ef in final_states
