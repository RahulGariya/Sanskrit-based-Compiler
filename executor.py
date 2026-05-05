from ast_nodes import *

def execute(ast):
    # This acts as our computer's RAM, storing variable names and their values
    memory = {}

    def eval_expr(node):
        if isinstance(node, Num):
            return node.value

        if isinstance(node, Str):
            return node.value

        if isinstance(node, Var):
            # Default to 0 if the variable hasn't been assigned yet
            return memory.get(node.name, 0)

        # --- NEW: UNARY OPERATOR (NOT) ---
        if isinstance(node, UnaryOp):
            expr_val = eval_expr(node.expr)
            if node.op == "NOT": 
                return not bool(expr_val)

        if isinstance(node, BinOp):
            l = eval_expr(node.left)
            r = eval_expr(node.right)

            # Math & Comparisons
            if node.op == "PLUS": return l + r
            if node.op == "MINUS": return l - r
            if node.op == "MUL": return l * r
            if node.op == "DIV": return l // r
            if node.op == "GT": return l > r
            if node.op == "LT": return l < r
            
            # --- NEW: LOGICAL OPERATIONS ---
            if node.op == "AND": return bool(l) and bool(r)
            if node.op == "OR":  return bool(l) or bool(r)
            if node.op == "XOR": return bool(l) ^ bool(r)
            # --- NEW: Array Evaluation ---
        if isinstance(node, ArrayDecl):
            # Evaluate all items inside the brackets and return a Python list
            return [eval_expr(e) for e in node.elements]
            
        if isinstance(node, ArrayAccess):
            # Get the array from memory and pull the correct index
            arr = memory.get(node.name, [])
            idx = eval_expr(node.index)
            return arr[idx]


    def run_block(block):
        for stmt in block:
            run(stmt)

    def run(stmt):
        if isinstance(stmt, Assign):
            memory[stmt.name] = eval_expr(stmt.value)

        elif isinstance(stmt, Print):
            # Print to standard output (the terminal)
            print(eval_expr(stmt.value))

        elif isinstance(stmt, If):
            if eval_expr(stmt.condition):
                run_block(stmt.body)
            else:
               
                executed_elif = False
                for elif_cond, elif_body in stmt.elifs:
                    if eval_expr(elif_cond):
                        run_block(elif_body)
                        executed_elif = True
                        break 
               
                if not executed_elif:
                    run_block(stmt.else_body)


        elif isinstance(stmt, While):
            # Evaluates the 'cond' from the AST While node
            while eval_expr(stmt.condition):
                run_block(stmt.body)
        elif isinstance(stmt, Input):
            user_val = input(f">> Please enter a value for '{stmt.name}': ")
            # Automatically convert to an integer if the user typed a number
            if user_val.lstrip('-').isdigit(): 
                memory[stmt.name] = int(user_val)
            else:
                memory[stmt.name] = user_val

        elif isinstance(stmt, If):
            if eval_expr(stmt.cond): run_block(stmt.body)
            else: run_block(stmt.else_body)

        elif isinstance(stmt, While):
            while eval_expr(stmt.cond): run_block(stmt.body)
        
        # --- NEW: Array Assignment ---
        elif isinstance(stmt, ArrayAssign):
            idx = eval_expr(stmt.index)
            val = eval_expr(stmt.value)
            memory[stmt.name][idx] = val

    # Start execution by running every statement in the main AST list
    for stmt in ast:
        run(stmt)