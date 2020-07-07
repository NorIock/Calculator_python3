#! /usr/bin/env python3
# coding: utf-8

#Generate the widow
from tkinter import *
from tkinter import messagebox
from math import *

window = Tk()
window.title("Renaud's calculator in python 3")
window.configure(background="light grey")

calc_input = ""
rpn_calc_input = ""

# Create in a dictionnary the basics operations with anonymous functions (lambda)
ops = {
    "+": (lambda a, b: a + b),
    "-": (lambda a, b: a - b),
    "*": (lambda a, b: a * b),
    "/": (lambda a, b: a / b),
    "^": (lambda a, b: a ** b),
    "√": (lambda a, b: b ** (1 / a))
}

# Create in dictionnary functions which take one parameter only
funcs = {
    "sin": (lambda a: sin(a)),
    "cos": (lambda a: cos(a)),
    'tan': (lambda a: tan(a)),
    'log': (lambda a: log(a)),
    'ln': (lambda a: ln(a))
}

# Manage priority during calculation: ^ firts then * and / before + and -
priorities = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "^": 3,
    "√": 3
}

# Record all the inputs on the calculator
def input_key(value):
    global calc_input
    calc_input += value
    calc_input_text.set(calc_input)
    print(calc_input)

# A function which will convert the operation in RPN (Reverse Polish Notation)
def rpn() -> str:
    
    global calc_input
    global rpn_calc_input

    # Use of split to examine each component one by one
    tokens = calc_input.split()

    # We need two stackes to convert, one for operators, another for the final output in rpn
    operators = []
    output = []

    for token in tokens:

        # Search for numbers in tokens to add them to the output stack
        if token.isnumeric():
            output.append(token)
            continue

        #Search for funcs in tokens
        if token in funcs:
            operators.append(token)
            continue
        
        # Search for operators in tokens to add them in the operator stack and then transfer them to the output stack
        # len(operators) is essential. If operators is empty the number will be taken before the function
        if token in ops:
            while (len(operators) and
            operators[-1] != "(" and 
            (operators[-1] in funcs or
            priorities[operators[-1]] > priorities[token])):
                output.append(operators.pop())

            operators.append(token)
            continue 

        if token == "(":
            operators.append(token)
            continue

        if token == ")":
            while (len(operators) > 0 and operators[-1] != "("):
                output.append(operators.pop())
            
            if len(operators) == 0:
                raise Exception("mismatching parenthesis")
        
            operators.pop()
            continue

        raise Exception('unknown token: {}'.format(token))

    while (len(operators)):
        output.append(operators.pop())
        # Handling other exception like divide by 0
        if output[-1] == '/' and output[-2] == '0':
            raise Exception("You can't divide by zero")
    

    result = " "
    rpn_calc_input = result.join(output)
    print(rpn_calc_input)
    calc_input = ""

    return rpn_calc_input

def equal():

    global rpn_calc_input
    result = 0
    
    rpn()

    tokens = rpn_calc_input.split()
    # The stack will allow to temporaly save the results during the whole calculation
    stack = []

    #Search for the operators
    for token in tokens:

        if token in ops:
            # Taking the 2 numbers previously stored in stack (see else: for details)
            nbr2 = float(stack.pop())
            nbr1 = float(stack.pop())
            # Calculation and storage in stack waiting for others calculations
            result = ops[token](nbr1, nbr2)
            stack.append(result)

        elif token in funcs:
            nbr = float(stack.pop())
            result = funcs[token](nbr)
            stack.append(result)

        else:
            stack.append(token)
    
    # result = stack[0]
    
    calc_input = ""
    rpn_calc_input = ""
    calc_input_text.set(calc_input)
    result_text.set(stack[0])
    print(stack[0])
    print(calc_input)
    return

# Clear the inputs in case of mistake
def clear():
    global calc_input
    calc_input = ""
    calc_input_text.set(calc_input)

def guide():
    messagebox.showinfo('How to use', 'Simple as a regular calculator except that you have to use the space button between each entry. For example to calculate 10 + 2 power 2, you will have to do 10 space + space 2 space power space 2')

#Generate the buttons
Button(window, text="Guide", command= guide(), bg="black", fg ="white").grid(row= 0, column = 0)
Button(window, text="Close", command=window.quit, bg="black", fg ="white").grid(row= 0, column = 3)
Button(window, text="0", command=lambda: input_key("0"), bg="burlywood").grid(row= 8, column = 0)
Button(window, text="space", command=lambda: input_key(" "), bg="darkslategray", fg ="white").grid(row= 8, column = 1)
Button(window, text="AC", command=lambda: clear(), bg="darkslategray", fg ="white").grid(row= 8, column = 2)
Button(window, text=" 1 ", command=lambda: input_key("1"), bg="burlywood").grid(row= 7, column = 0)
Button(window, text=" 2 ", command=lambda: input_key("2"), bg="burlywood").grid(row= 7, column = 1)
Button(window, text=" 3 ", command=lambda: input_key("3"), bg="burlywood").grid(row= 7, column = 2)
Button(window, text=" 4 ", command=lambda: input_key("4"), bg="burlywood").grid(row= 6, column = 0)
Button(window, text=" 5 ", command=lambda: input_key("5"), bg="burlywood").grid(row= 6, column = 1)
Button(window, text=" 6 ", command=lambda: input_key("6"), bg="burlywood").grid(row= 6, column = 2)
Button(window, text=" 7 ", command=lambda: input_key("7"), bg="burlywood").grid(row= 5, column = 0)
Button(window, text=" 8 ", command=lambda: input_key("8"), bg="burlywood").grid(row= 5, column = 1)
Button(window, text=" 9 ", command=lambda: input_key("9"), bg="burlywood").grid(row= 5, column = 2)
Button(window, text=" + ", command=lambda: input_key("+"), bg="goldenrod").grid(row= 6, column = 3)
Button(window, text=" - ", command=lambda: input_key("-"), bg="goldenrod").grid(row= 6, column = 4)
Button(window, text=" * ", command=lambda: input_key("*"), bg="goldenrod").grid(row= 5, column = 3)
Button(window, text=" / ", command=lambda: input_key("/"), bg="goldenrod").grid(row= 5, column = 4)
Button(window, text=" = ", command=lambda: equal(), bg="darkslategray", fg ="white").grid(row= 7, column = 3)
Button(window, text="sin", command=lambda: input_key("sin"), bg="sienna").grid(row= 4, column = 0)
Button(window, text="cos", command=lambda: input_key("cos"), bg="sienna").grid(row= 4, column = 1)
Button(window, text="tan", command=lambda: input_key("tan"), bg="sienna").grid(row= 4, column = 2)
Button(window, text="log", command=lambda: input_key("log"), bg="sienna").grid(row= 4, column = 3)
Button(window, text="ln", command=lambda: input_key("ln"), bg="sienna").grid(row= 4, column = 4)
Button(window, text=" ^ ", command=lambda: input_key("^"), bg="sienna").grid(row= 3, column = 0)
Button(window, text=" n√ ", command=lambda: input_key("√"), bg="sienna").grid(row= 3, column = 1)
Button(window, text=" ( ", command=lambda: input_key("("), bg="cornsilk").grid(row= 3, column = 3)
Button(window, text=" ) ", command=lambda: input_key(")"), bg="cornsilk").grid(row= 3, column = 4)

calc_input_text = StringVar()
Label(window, textvariable=calc_input_text).grid(row=1, column=0)
result_text = StringVar()
Label(window, textvariable=result_text).grid(row=2, column=0)
window.mainloop()
