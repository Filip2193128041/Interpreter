# INTERPRETER.PY -- ANNOTATED VERSION
# This file contains FOUR separate mini-interpreters, each more
# advanced than the last. Bugs from the original file are fixed here
# and marked with "FIXED:" comments so you can spot what changed.



tokens = []        # the current line's tokens live here, refilled each run()
pos = 0             # the "cursor" -- index of the token we're about to read
variables = {}      # global symbol table: variable name -> value

program = """
a = 5
b = a + 3
c = b + a
print c
print a + b + 2
"""  # the mini-program we will execute line by line


def tokenize(text):
    # Pads every operator/paren with spaces, then splits on whitespace.
    # "a=5+3" -> "a = 5 + 3" -> ["a", "=", "5", "+", "3"]
    # Without the padding, "a=5" would be one unsplittable chunk.
    return (
        text.replace("=", " = ")
        .replace("+", " + ")
        .replace("-", " - ")
        .replace("*", " * ")
        .replace("/", " / ")
        .replace("(", " ( ")
        .replace(")", " ) ")
        .split()
    )


def peek():
    # Look at the current token WITHOUT moving the cursor forward.
    if pos < len(tokens):
        return tokens[pos]
    return None  # ran off the end of the token list


def next_token():
    # Look at the current token AND advance the cursor by one.
    global pos
    token = peek()
    pos += 1
    return token


def get_lit():
    # Reads ONE literal: either a number ("5" -> 5) or a known variable.
    token = next_token()
    if token.isdigit():
        return int(token)
    if token in variables:
        return variables[token]
    raise Exception(f"Unknown lit: {token}")


def get_expr():
    # Reads a literal, then optionally ONE operator and another literal.
    # LIMITATION: only handles a single operation (a + b), not a + b + c.
    left = get_lit()
    if peek() in ["+", "-", "*", "/"]:
        op = next_token()
        right = get_lit()
        if op == "+":
            return left + right
        if op == "/":
            return left / right
        if op == "*":
            return left * right
        if op == "-":
            return left - right
    return left  # no operator found -- just return the literal


def run(line):
    # Executes a single line: either "print <expr>" or "name = <expr>".
    global tokens, pos
    tokens = tokenize(line)   # re-tokenize fresh for this line
    pos = 0                   # reset cursor to the start
    if peek() == "print":
        next_token()           # consume the word "print"
        print(get_expr())      # evaluate and print the rest of the line
        return
    name = next_token()        # the variable being assigned
    if next_token() != "=":
        raise Exception("Im expecting a '=' ")
    val = get_expr()           # evaluate the right-hand side
    variables[name] = val      # store it in the global symbol table


def run_program(program):
    # Splits the whole program into lines and runs each one in order.
    for line in program.split('\n'):
        line = line.strip()
        if line == "":
            continue            # skip blank lines
        run(line)


run_program(program)  # actually executes Part 1's demo program



class Stack:
    # A classic last-in-first-out stack, used to evaluate RPN expressions.
    def __init__(self):
        self.items = []  # underlying storage

    def push(self, value):
        self.items.append(value)  # add to the top

    def append(self, value):
        # Alias so .append() works the same as .push() if you forget which.
        self.push(value)

    def pop(self):
        if len(self.items) == 0:
            raise Exception('stack underflow')  # can't pop from empty stack
        return self.items.pop()

    def peek(self):
        if len(self.items) == 0:
            raise Exception("Stack is empty")
        return self.items[-1]  # look at top without removing it

    def dup(self):
        # Duplicate the top item (common RPN/Forth operation).
        top = self.peek()
        self.push(top)

    def swap(self):
        # Swap the top two items in place.
        if len(self.items) < 2:
            raise Exception("I need at least 2 values to swap...")
        self.items[-1], self.items[-2] = self.items[-2], self.items[-1]

    def __repr__(self):
        # Lets you print(stack) and see something readable.
        return str(self.items)

    def __getitem__(self, index):
        # Lets you do stack[-1] directly instead of stack.items[-1].
        return self.items[index]


class RPNInterpreter:
    # Evaluates expressions written in Reverse Polish Notation,
    # e.g. "3 4 +" instead of "3 + 4". No precedence rules needed --
    # the order of tokens IS the order of operations.
    def __init__(self):
        self.stack = Stack()      # this interpreter's own stack
        self.variables = {}        # this interpreter's own variables (NOT global)

    def get_value(self, token):
        # Resolves a token to either a literal int or a stored variable.
        if token.isdigit():
            return int(token)
        if token in self.variables:
            return self.variables[token]
        raise Exception(f"Unknown token: {token}")

    def run_rpn(self, exp):
        # Walks tokens left to right. Numbers get pushed; operators pop
        # two values, combine them, and push the result back.
        tokens = exp.split()
        for token in tokens:
            if token.isdigit():
                self.stack.push(int(token))
            elif token in self.variables:
                self.stack.push(self.variables[token])
            elif token in ["+", "-", "*", "/"]:
                b = self.stack.pop()  # second operand (pushed last)
                a = self.stack.pop()  # first operand (pushed first)
                if token == "+":
                    self.stack.push(a + b)
                elif token == "/":
                    self.stack.push(a / b)
                elif token == "*":
                    self.stack.push(a * b)
                elif token == "-":
                    self.stack.push(a - b)
            else:
                raise Exception(f"Unknown token: {token}")
        return self.stack[-1]  # final answer sits on top of the stack

    def run_line(self, line):
        # Dispatches a line to: print, assignment, or raw RPN evaluation.
        line = line.strip()
        if line.startswith("print "):
            exp = line[6:]                  # everything after "print "
            print(self.run_rpn(exp))
        elif "=" in line:
            name, exp = line.split("=", 1)  # split on FIRST "=" only
            name = name.strip()
            exp = exp.strip()
            value = self.run_rpn(exp)
            self.variables[name] = value
        else:
            self.run_rpn(line)              # just evaluate, don't store


interpreter = RPNInterpreter()
interpreter.run_line("a = 3 4 +")   # a = 7
interpreter.run_line("b = a 2 *")   # b = 14
interpreter.run_line("print b")     # prints 14



# This is the "proper" way to handle operator precedence: + and - are
# handled by parse_expression, * and / by parse_term, and individual
# numbers/parens by parse_factor. Each level calls the level "below" it
# first, which naturally makes * and / bind tighter than + and -.

def parse_expression():
    # Handles + and - (lowest precedence -- evaluated last)
    left = parse_term()
    while peek() in ['+', '-']:
        op = next_token()
        right = parse_term()
        left = (op, left, right)  # build a tuple node, e.g. ('+', 3, 4)
    return left


def parse_term():
    # Handles * and / (higher precedence -- evaluated first)
    left = parse_factor()
    while peek() in ['*', '/']:
        op = next_token()
        right = parse_factor()
        left = (op, left, right)
    return left


def parse_factor():
    # Handles the smallest units: numbers, variables, or (parenthesized
    # sub-expressions).
    token = next_token()
    if token is None:
        raise SyntaxError("Unexpected end of input")
    if token.isdigit():
        return int(token)
    if token == '(':
        val = parse_expression()   # recurse back to the TOP for what's inside ()
        if peek() != ')':
            raise SyntaxError("Expected ')'")
        next_token()                # consume the ')'
        return val
    return token  # not a digit or '(' -- treat it as a variable name (string)


def evaluate(node):
    # Walks the tree (made of nested tuples) and computes the result.
    if isinstance(node, int):
        return node                       # base case: plain number
    if isinstance(node, str):
        return variables[node]            # base case: variable lookup
    op, left, right = node                # recursive case: ('+', left, right)
    if op == '+':
        return evaluate(left) + evaluate(right)
    if op == '/':
        return evaluate(left) / evaluate(right)
    if op == '*':
        return evaluate(left) * evaluate(right)
    if op == '-':
        return evaluate(left) - evaluate(right)
    raise Exception(f"Unknown operator: {op}")

# 
# SAME PARSER, BUT WRAPPED IN A CLASS

# tokens/pos/variables, so multiple parsers can coexist safely.

class Parser:
    def __init__(self, text):
        self.tokens = tokenize(text)   # this parser's own token list
        self.pos = 0                   # this parser's own cursor
        self.variables = {}            # this parser's own variable table
        # FIXED: original __init__ didn't have self.variables, so
        # evaluate() had nothing of its own to look variables up in.

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def next_token(self):
        token = self.peek()
        self.pos += 1
        return token

    def parse_expression(self):
        # FIXED: original called bare peek()/next_token()/parse_term()
        # (the global Part-3 functions) instead of self.<method>() --
        # that would crash with NameError as soon as it hit '+' or '-'.
        left = self.parse_term()
        while self.peek() in ['+', '-']:
            op = self.next_token()
            right = self.parse_term()
            left = (op, left, right)
        return left

    def parse_term(self):
        # FIXED: original watched for ['+','-'] here (wrong -- that's
        # parse_expression's job) and recursed into self.parse_term()
        # instead of self.parse_factor(), causing infinite recursion.
        left = self.parse_factor()
        while self.peek() in ['*', '/']:
            op = self.next_token()
            right = self.parse_factor()
            left = (op, left, right)
        return left

    def parse_factor(self):
        token = self.next_token()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        if token.isdigit():
            return int(token)
        elif token == '(':
            expr = self.parse_expression()
            if self.next_token() != ')':
                raise SyntaxError("Im expecting a ')'. ")
            return expr
        raise SyntaxError(f"Unexpected token: {token}")

    def parse(self):
        # Convenience entry point: resets cursor and parses the whole thing.
        self.pos = 0
        return self.parse_expression()

    def evaluate(self, node):
        # FIXED: original was missing `self`, so it couldn't be called
        # as parser.evaluate(tree) -- Python would've passed `tree` in
        # as if it were `self`, then crashed unpacking `op,left,right`.
        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return self.variables[node]   # uses THIS parser's variables
        op, left, right = node
        if op == '+':
            return self.evaluate(left) + self.evaluate(right)
        if op == '-':
            return self.evaluate(left) - self.evaluate(right)
        if op == '/':
            return self.evaluate(left) / self.evaluate(right)
        if op == '*':
            return self.evaluate(left) * self.evaluate(right)
        raise Exception(f"Unknown operator: {op}")


# Demo: class-based parser end to end.
parser = Parser("3 + 4 * 2")
res = parser.parse()
print(parser.evaluate(res))  # 11


# TEST CASES for Part 3 (the free-function recursive descent parser)

print("Running tests.....")

tokens = tokenize("3 + 4 * 2")
pos = 0
tree = parse_expression()
print(evaluate(tree))  # 11

tokens = tokenize("( 3 + 4 ) * 2")
pos = 0
tree = parse_expression()
print(evaluate(tree))  # 14

variables['a'] = 5
tokens = tokenize("a + 3 * 2")
pos = 0
tree = parse_expression()
print(evaluate(tree))  # 11
