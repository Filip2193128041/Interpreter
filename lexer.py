NUMBER  = "NUMBER"   # a numeric literal
IDENT   = "IDENT"    # a variable/name:          a
OP      = "OP"       # an arithmetic operator:   + - * /
EQUALS  = "EQUALS"   # assignment:               =
LPAREN  = "LPAREN"   # open parenthesis:         (
RPAREN  = "RPAREN"   # close parenthesis:        )
EOF     = "EOF"      # end of input 


class Token:
    def __init__(self, type, value):
        self.type  = type   
        self.value = value   
 
    def __repr__(self):
        # Makes print(token) readable, e.g.  Token(NUMBER, 42)
        return f"Token({self.type}, {self.value!r})"
class Lexer:
    def __init__(self, text):
        self.text = text   # the raw source string we are scanning
        self.pos  = 0      # cursor: index of the CURRENT character

    def current(self):
        # Return the character at the cursor, or None if past the end.
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None
 
    def advance(self):
        # Move the cursor forward by one character.
        self.pos += 1
 
    def skip_whitespace(self):
        # Keep advancing while the current character is a space or tab.
        while self.current() is not None and self.current() in ' \t':
            self.advance()
