from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    LAMBDA = auto()
    DOT = auto()
    LPAREN = auto()
    RPAREN = auto()
    VARIABLE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def peek(self) -> str:
        return self.text[self.pos] if self.pos < len(self.text) else ""

    def advance(self):
        self.pos += 1

    def skip_spaces(self):
        while self.pos < len(self.text) and self.peek() in " \t\n\r":
            self.advance()

    def read_variable(self) -> str:
        if not (self.peek().isalpha() or self.peek() == "_"):
            raise SyntaxError("Variable must start with letter or underscore")
        start = self.pos
        while self.pos < len(self.text) and (self.peek().isalnum() or self.peek() == "_"):
            self.advance()
        return self.text[start:self.pos]

    def next_token(self) -> Token:
        self.skip_spaces()
        c = self.peek()

        if c == "":
            return Token(TokenType.EOF, "")

        if c in ("λ", "\\"):
            self.advance()
            return Token(TokenType.LAMBDA, c)

        if c == ".":
            self.advance()
            return Token(TokenType.DOT, ".")

        if c == "(":
            self.advance()
            return Token(TokenType.LPAREN, "(")

        if c == ")":
            self.advance()
            return Token(TokenType.RPAREN, ")")

        if c.isalpha() or c == "_":
            return Token(TokenType.VARIABLE, self.read_variable())

        raise SyntaxError(f"Unexpected character: {c}")

    def tokenize(self):
        tokens = []
        while True:
            t = self.next_token()
            tokens.append(t)
            if t.type == TokenType.EOF:
                break
        return tokens


@dataclass
class Var:
    name: str

    def __str__(self):
        return self.name

    def free_vars(self):
        return {self.name}

    def substitute(self, var, expr):
        return expr if self.name == var else self


@dataclass
class Abs:
    param: str
    body: "Expr"

    def __str__(self):
        return f"(λ{self.param}.{self.body})"

    def free_vars(self):
        return self.body.free_vars() - {self.param}

    def substitute(self, var, expr):
        if self.param == var:
            return self

        if self.param in expr.free_vars():
            new = self._fresh(self.param, expr.free_vars() | self.body.free_vars())
            renamed_body = self.body.substitute(self.param, Var(new))
            new_body = renamed_body.substitute(var, expr)
            return Abs(new, new_body)

        return Abs(self.param, self.body.substitute(var, expr))

    def _fresh(self, base, avoid):
        if base not in avoid:
            return base
        i = 1
        while f"{base}{i}" in avoid:
            i += 1
        return f"{base}{i}"


@dataclass
class App:
    func: "Expr"
    arg: "Expr"

    def __str__(self):
        return f"({self.func} {self.arg})"

    def free_vars(self):
        return self.func.free_vars() | self.arg.free_vars()

    def substitute(self, var, expr):
        return App(self.func.substitute(var, expr), self.arg.substitute(var, expr))


Expr = Var | Abs | App


class Parser:
    def __init__(self, lexer):
        self.tokens = lexer.tokenize()
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token(TokenType.EOF, "")

    def advance(self):
        self.pos += 1

    def expect(self, token_type):
        tok = self.peek()
        if tok.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {tok.type} at position {self.pos}")
        self.advance()
        return tok

    def parse_expression(self):
        tok = self.peek()

        if tok.type == TokenType.VARIABLE:
            self.advance()
            return Var(tok.value)

        if tok.type == TokenType.LPAREN:
            self.advance()

            if self.peek().type == TokenType.LAMBDA:
                self.advance()
                var_name = self.expect(TokenType.VARIABLE).value
                self.expect(TokenType.DOT)
                body = self.parse_expression()
                self.expect(TokenType.RPAREN)
                return Abs(var_name, body)

            func = self.parse_expression()
            arg = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return App(func, arg)

        raise SyntaxError(f"Unexpected token: {tok.type} at position {self.pos}")

    def parse(self):
        expr = self.parse_expression()
        if self.peek().type != TokenType.EOF:
            raise SyntaxError(f"Trailing tokens after expression at position {self.pos}")
        return expr


class Normalizer:
    def __init__(self, max_steps=100_000):
        self.max_steps = max_steps
        self.steps = 0

    def normalize(self, expr):
        self.steps = 0
        return self._norm(expr)

    def _norm(self, expr):
        while True:
            if self.steps >= self.max_steps:
                raise RuntimeError("Too many reduction steps")
            new, changed = self._step(expr)
            if not changed:
                return expr
            expr = new
            self.steps += 1

    def _step(self, expr):
        if isinstance(expr, Var):
            return expr, False

        if isinstance(expr, Abs):
            new_body, changed = self._step(expr.body)
            return Abs(expr.param, new_body), changed

        if isinstance(expr, App):
            if isinstance(expr.func, Abs):
                r = expr.func.body.substitute(expr.func.param, expr.arg)
                return r, True
            f2, changed = self._step(expr.func)
            if changed:
                return App(f2, expr.arg), True
            a2, changed = self._step(expr.arg)
            if changed:
                return App(expr.func, a2), True
            return expr, False

        return expr, False
