tokens= []
pos=0 
variables= {}


program= """
a = 5
b = a + 3
c = b + a
print c
print a + b + 2
"""


def tokenize(text):
    return text.replace("=", " = ").replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ").replace("(", " ( ").replace(")", " ) ").split()

def peek():
    if pos < len(tokens):
        return tokens[pos]
    return None

def next_token():
    global pos
    token = peek()
    pos += 1 
    return token

def get_lit():
    token = next_token()
    if token.isdigit():
        return int(token)
    if token in variables:
        return variables[token]
    raise Exception(f"Unknown lit: {token}")

def get_expr():
    left = get_lit()
    if peek() in ["+","-","*","/"]:
        op = next_token()
        right = get_lit()
        if op == "+": return left + right
        if op == "/": return left / right
        if op == "*": return left * right
        if op == "-": return left - right
    return left

def run(line):
    global tokens, pos
    tokens = tokenize(line)
    pos = 0
    if peek() == "print":
        next_token()
        print(get_expr())
        return
    name = next_token()
    if next_token() != "=":
        raise Exception("Im expecting a '=' ")
    val = get_expr()
    variables[name] = val

def run_program(program):
    for line in program.split('\n'):
        line = line.strip()
        if line == "":
            continue
        run(line)

run_program(program)


class Stack:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def append(self, value):
        self.push(value)

    def pop(self):
        if len(self.items) == 0:
            raise Exception('stack underflow')
        return self.items.pop()
    
    def peek(self):
        if len(self.items) == 0:
            raise Exception("Stack is empty")
        return self.items[-1]
    
    def dup(self):
        top = self.peek()
        self.push(top)

    def swap(self):
        if len(self.items) < 2:
            raise Exception("I need at least 2 values to swap...")
        self.items[-1], self.items[-2] = self.items[-2], self.items[-1]

    def __repr__(self):
        return str(self.items)
    
    def __getitem__(self, index):
        return self.items[index]


class RPNInterpreter:
    def __init__(self):
        self.stack = Stack()
        self.variables = {}

    def get_value(self, token):
        if token.isdigit():
            return int(token)
        if token in self.variables:
            return self.variables[token]
        raise Exception(f"Unknown token: {token}")
    
    def run_rpn(self, exp):
        tokens = exp.split()
        for token in tokens:
            if token.isdigit():
                self.stack.push(int(token))
            elif token in self.variables:
                self.stack.push(self.variables[token])
            elif token in ["+","-","*","/"]:
                b = self.stack.pop()
                a = self.stack.pop()
                if token == "+": self.stack.push(a + b)
                elif token == "/": self.stack.push(a / b)
                elif token == "*": self.stack.push(a * b)
                elif token == "-": self.stack.push(a - b)
            else:
                raise Exception(f"Unknown token: {token}")
        return self.stack[-1]
    
    def run_line(self, line):
        line = line.strip()
        if line.startswith("print "):
            exp = line[6:]
            print(self.run_rpn(exp))
        elif "=" in line:
            name, exp = line.split("=", 1)
            name = name.strip()
            exp = exp.strip()
            value = self.run_rpn(exp)
            self.variables[name] = value
        else:
            self.run_rpn(line)


interpreter = RPNInterpreter()
interpreter.run_line("a = 3 4 +")
interpreter.run_line("b = a 2 *")
interpreter.run_line("print b")



def parse_expression():
    left = parse_term()
    while peek() in ['+', '-']:
        op = next_token()
        right = parse_term()
        left = (op, left, right)
    return left

def parse_term():
    left = parse_factor()
    while peek() in ['*', '/']:
        op = next_token()
        right = parse_factor()
        left = (op, left, right)
    return left

def parse_factor():
    token = next_token()
    if token is None:
        raise SyntaxError("Unexpected end of input")
    if token.isdigit():
        return int(token)
    if token == '(':
        val = parse_expression()
        if peek() != ')':
            raise SyntaxError("Expected ')'")
        next_token()
        return val
    return token

def evaluate(node):
    if isinstance(node, int):
        return node
    if isinstance(node, str):
        return variables[node]
    op, left, right = node
    if op == '+': return evaluate(left) + evaluate(right)
    if op == '/': return evaluate(left) / evaluate(right)
    if op == '*': return evaluate(left) * evaluate(right)
    if op == '-': return evaluate(left) - evaluate(right)
    raise Exception(f"Unknown operator: {op}")


class Parser:
    def __init__(self, text):
        self.tokens = tokenize(text)
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def next_token(self):
        token = self.peek()
        self.pos += 1
        return token
    
    def parse_expression(self):
        left = self.parse_term()
        while peek() in ['+', '-']:
            op = next_token()
            right = parse_term()
            left = (op, left, right)
        return left
    
    def parse_term(self):
        left= self.parse_factor()
        while self.peek() in ['+','-']:
            op= self.next_token()
            right= self.parse_term()
            left= (op,left,right)
        return left 
    
    def parse_factor(self):
        token= self.next_token()

        if token.isdigit():
            return int(token)
        
        elif token == '(':
            expr= self.parse_expression()

            if self.next_token() != ')':
                raise SyntaxError("Im expecting a ')'. ")
            
            return expr
        
        raise SyntaxError(f"Unexpected token: {token}")
    
    def parse(self):
        return self.parse_expression()
    
    def evaluate(node):
        if isinstance(node,int):
            return node
        if isinstance(node,str):
            return variables[node]
        
        op,left,right= node
        if op =='+': return evaluate(left) + evaluate(right)
        if op == '-': return evaluate(left) - evaluate(right)
        if op == '/': return evaluate(left) / evaluate(right)
        if op == '*': return evaluate(left) * evaluate(right)
        
    

tokens= tokenize("3 + 4  * 2")

parser= Parser("3 + 4 * 2")
res= parser.parse()
print(res)


    


    

        
        



#test case
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
