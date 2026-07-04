NUMBER  = "NUMBER"   # a numeric literal:        5, 42, 3.14
IDENT   = "IDENT"    # a variable/name:          a, myVar, x1
OP      = "OP"       # an arithmetic operator:   + - * /
EQUALS  = "EQUALS"   # assignment:               =
LPAREN  = "LPAREN"   # open parenthesis:         (
RPAREN  = "RPAREN"   # close parenthesis:        )
EOF     = "EOF"      # end of input -- sentinel so peek() never returns None


class Token:
    def __init__(self, type, value):
        self.type  = type    # one of the constants above, e.g. NUMBER
        self.value = value   # the actual payload, e.g. 42 or "+" or "myVar"
 
    def __repr__(self):
        # Makes print(token) readable, e.g.  Token(NUMBER, 42)
        return f"Token({self.type}, {self.value!r})"
