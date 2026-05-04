class Node: pass

class Assign(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Print(Node):
    def __init__(self, value):
        self.value = value

class If:
    def __init__(self, condition, body, elifs, else_body):
        self.condition = condition
        self.body = body
        self.elifs = elifs        
        self.else_body = else_body

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(Node):
    def __init__(self, value):
        self.value = int(value)

class Str(Node):
    def __init__(self, value):
        self.value = value

class Var(Node):
    def __init__(self, name):
        self.name = name

class UnaryOp:
    def __init__(self, op, expr):
        self.op = op       # E.g., 'NOT'
        self.expr = expr   # E.g., the variable or condition being inverted

class Input:
    def __init__(self, name):
        self.name = name        