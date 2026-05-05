from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, type_):
        token = self.current()
        if token and token[0] == type_:
            self.pos += 1
            return token
        raise Exception(f"Expected {type_}, got {token}")

    def parse(self):
        stmts = []
        while self.current():
            stmts.append(self.statement())
        return stmts

    def statement(self):
        tok = self.current()

        if tok[0] == "ID":
            return self.assignment()
        elif tok[0] == "PRINT":
            return self.print_stmt()
        elif tok[0] == "INPUT":          
            return self.input_stmt()
        elif tok[0] == "IF":
            return self.if_stmt()
        elif tok[0] == "WHILE":
            return self.while_stmt()
        else:
            raise Exception("Invalid statement")

    def input_stmt(self):
        self.eat("INPUT")
        var_name = self.eat("ID")[1]
        self.eat("SEMI")
        return Input(var_name)

    def block(self):
        stmts = []
        self.eat("LBRACE")
        while self.current()[0] != "RBRACE":
            stmts.append(self.statement())
        self.eat("RBRACE")
        return stmts

    def if_stmt(self):
        self.eat("IF")
        condition = self.expr()
        self.eat("THEN")
        body = self.block()

        elifs = []
        while self.current() and self.current()[0] == "ELSEIF":
            self.eat("ELSEIF")
            elif_cond = self.expr()
            self.eat("THEN")
            elif_body = self.block()
            elifs.append((elif_cond, elif_body))

        # Final ELSE block
        else_body = []
        if self.current() and self.current()[0] == "ELSE":
            self.eat("ELSE")
            else_body = self.block()

        self.eat("SEMI") 
        return If(condition, body, elifs, else_body)

    def while_stmt(self):
        self.eat("WHILE")
        cond = self.expr()
        self.eat("THEN")
        body = self.block()
        self.eat("SEMI")
        return While(cond, body)

    def assignment(self):
        name = self.eat("ID")[1]
        
        if self.current() and self.current()[0] == "LBRACK":
            self.eat("LBRACK")
            index = self.expr()
            self.eat("RBRACK")
            self.eat("EQ")
            val = self.expr()
            self.eat("SEMI")
            return ArrayAssign(name, index, val)
            
        self.eat("EQ")
        val = self.expr()
        self.eat("SEMI")
        return Assign(name, val)

    def print_stmt(self):
        self.eat("PRINT")
        val = self.expr()
        self.eat("SEMI")
        return Print(val)

    # --- EXPRESSION PARSING (ORDER OF OPERATIONS) ---
    
    def expr(self):
        # Lowest precedence: OR
        return self.logical_or()

    def logical_or(self):
        left = self.logical_and()
        while self.current() and self.current()[0] == "OR":
            op = self.eat("OR")[0]
            right = self.logical_and()
            left = BinOp(left, op, right) 
        return left

    def logical_and(self):
        left = self.logical_not()
        while self.current() and self.current()[0] in ("AND", "XOR"):
            op = self.eat(self.current()[0])[0]
            right = self.logical_not()
            left = BinOp(left, op, right)
        return left

    def logical_not(self):
        # NOT is a unary operator (only takes one argument, to its right)
        if self.current() and self.current()[0] == "NOT":
            op = self.eat("NOT")[0]
            right = self.logical_not() 
            return UnaryOp(op, right)
        return self.comparison()

    def comparison(self):
        left = self.arithmetic()
        while self.current() and self.current()[0] in ("GT", "LT"):
            op = self.eat(self.current()[0])[0]
            right = self.arithmetic()
            left = BinOp(left, op, right)
        return left

    def arithmetic(self):
        # This replaces your old expr() method
        left = self.term()
        while self.current() and self.current()[0] in ("PLUS", "MINUS"):
            op = self.eat(self.current()[0])[0]
            right = self.term()
            left = BinOp(left, op, right)
        return left

    def term(self):
        left = self.factor()
        while self.current() and self.current()[0] in ("MUL", "DIV"):
            op = self.eat(self.current()[0])[0]
            right = self.factor()
            left = BinOp(left, op, right)
        return left

    def factor(self):
        tok = self.current()

        if tok[0] == "NUMBER": return Num(self.eat("NUMBER")[1])
        if tok[0] == "STRING": return Str(self.eat("STRING")[1].strip('"'))
        
        # --- ARRAY DECLARATION FIX ---
        if tok[0] == "LBRACK":
            self.eat("LBRACK")
            elements = []
            if self.current() and self.current()[0] != "RBRACK":
                elements.append(self.expr())
                while self.current() and self.current()[0] == "COMMA":
                    self.eat("COMMA")
                    elements.append(self.expr())
            self.eat("RBRACK")
            return ArrayDecl(elements)

        if tok[0] == "ID":
            name = self.eat("ID")[1]
            
            if self.current() and self.current()[0] == "LBRACK":
                self.eat("LBRACK")
                index = self.expr()
                self.eat("RBRACK")
                return ArrayAccess(name, index)
            return Var(name) 

        if tok[0] == "LPAREN":
            self.eat("LPAREN")
            e = self.expr()
            self.eat("RPAREN")
            return e

        raise Exception(f"Invalid expression: {tok}")