# variables= {}

# def eval(exp):
#     tokens= exp.split()

#     if len(tokens) == 1:
#         token = tokens[0]

#         if token.isdigit():
#             return int(token)

#         if token in variables:
#             return variables[token]
        
#         raise NameError(f"Unknown variable: {token}")
#     result= get_val

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
    return text.replace("=", " = ").replace("+", " + ").split()

def peek():
    if pos < len(tokens):
        return tokens[pos]
    return None

def next_token():
    global pos
    token = peek()
    pos +=1 
    return token

def get_lit():
    token= next_token()

    if token.isdigit():
        return int(token)
    
    if token in variables:
        return variables[token]
    raise Exception(f"Unknown lit: {token}")

def get_expr():
    left= get_lit()

    if peek() in ["+","-","*","/"]:
        op= next_token()
        right= get_lit()
        if op == "+":
            return left + right
        if op == "/":
            return left / right
        if op == "*":
            return left * right
        if op == "-":
            return left - right
    return left

def run(line):
    global tokens,pos
    tokens= tokenize(line)
    pos=0
    if peek() == "print":
        next_token()
        print(get_expr())
        return
    
    name= next_token()

    if next_token() != "=":
        raise Exception("Im expecting a '=' ")
    val= get_expr()
    variables[name] = val


def run_program(program):
    for line in program.split('\n'):
        line= line.strip()

        if line == "":
            continue
        run(line)
run_program(program)    


# def rpn(exp):
#     stack = []

#     for token in exp.split():
#         if token.isdigit():
#             stack.append(int(token))

#         elif token in ["+","-","*","/"]:
#             b = stack.pop()
#             a = stack.pop()

        #     if token == "+":
        #         stack.append(a + b)
        #     elif token == "-":
        #         stack.append(a - b)
        #     elif token == "*":
        #         stack.append(a * b)
        #     elif token == "/":
        #         stack.append(a / b)
        # else:
        #     raise Exception(f"Unknown token: {token}")
        
#     return stack.pop()
# print("Trying rpn...")
# print(rpn("3 4 +")) #7
# print(rpn("3 4 + 2 *")) #14
# print(rpn("10 2 /")) # 5

class RPNInterpeter:
    def __init__(self):
        self.stack = Stack()
        self.variables = {}

    def get_value(self,token):
        if token.isdigit():
            return int(token)
        
        if token in self.variables:
            return self.variables[token]
        raise Exception(f"Unknown token: {token}")
    
    def run_rpn(self,exp):
        tokens= exp.split()

        for token in tokens:
            if token.isdigit():
                  self.stack.append(int(token))
            elif token in self.variables:
                self.stack.append(self.variables[token])

            elif token in ["+","-","*","/"]:
                b = self.stack.pop()
                a = self.stack.pop()

                if token == "+":
                    self.stack.append(a + b)
                elif token == "/":
                    self.stack.append(a / b)
                elif token == "*":
                    self.stack.append(a * b)
                elif token == "-":
                    self.stack.append(a - b)

                else:
                    raise Exception(f"Unknown token: {token}")
        return self.stack[-1]
    
    def run_line(self,line):
        line = line.strip()

        if line.startswith("print "):
            exp= line[6:] # index for print_ _ <- is 6 
            print(self.run_rpn(exp))

        elif "=" in line:
            name, exp = line.split("=", 1) #
            name= name.strip()
            exp= exp.strip()

            value= self.run_rpn(exp)
            self.variables[name]= value

        else:
            self.run_rpn(line)

interpreter= RPNInterpeter()

interpreter.run_line("a = 3 4 +")
interpreter.run_line("b = a 2 *")
interpreter.run_line("print b")


class Stack:
    def __init__(self):
        self.items= []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if len(self.items) == 0:
            raise Exception('stack underflw')
        return self.items.pop()
    
    def peek(self):
        if len(self.items) == 0:
            raise Exception("Stack = Empty")
        return self.items[-1]
    
    def dup(self):
        self.pop()

    def swap(self):
        if len(self.items) < 2:
            raise Exception("I need atleast 2 values to swap...")
        self.items[-1], self.items[-2] = self.items[-2] , self.items[-1]

    def __repr__(self):
        return str(self.items)
    
        


def parse_expression():
    left = parse_term()
    while peek() in ['+', '-']:
        op = next_token()
        right = parse_term()
        left = (op, left, right)  # build a tree node
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
    if token.isdigit(): return int(token)
    if token == '(':
        val = parse_expression()
        next_token()  # consume ')'
        return val
    return token  # variable name

