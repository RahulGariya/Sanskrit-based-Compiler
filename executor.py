from ast_nodes import *

def execute(ast):
    # This acts as our computer's RAM
    memory = {}

    def eval_expr(node):
        if isinstance(node, Num):
            return node.value

        if isinstance(node, Str):
            return node.value

        if isinstance(node, Var):
            return memory.get(node.name, 0)

        if isinstance(node, UnaryOp):
            expr_val = eval_expr(node.expr)
            if node.op == "NOT": 
                return not bool(expr_val)

        if isinstance(node, BinOp):
            l = eval_expr(node.left)
            r = eval_expr(node.right)
            if node.op == "PLUS":
                
                if isinstance(l, str) or isinstance(r, str):
                    return str(l) + str(r)
                
                return l + r
            if node.op == "MINUS": return l - r
            if node.op == "MUL": return l * r
            if node.op == "DIV": return l // r
            if node.op == "GT": return l > r
            if node.op == "LT": return l < r
            if node.op == "AND": return bool(l) and bool(r)
            if node.op == "OR":  return bool(l) or bool(r)
            if node.op == "XOR": return bool(l) ^ bool(r)

        if isinstance(node, ArrayDecl):
            return [eval_expr(e) for e in node.elements]
            
        if isinstance(node, ArrayAccess):
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
            print(eval_expr(stmt.value))

        elif isinstance(stmt, Input):
            val = input()
            try:
                # Convert to number if possible
                if '.' in val: val = float(val)
                else: val = int(val)
            except ValueError:
                pass 
            
            target = stmt.target
            if isinstance(target, Var):
                memory[target.name] = val
            elif isinstance(target, ArrayAccess):
                arr_name = target.name
                idx = eval_expr(target.index)
                if arr_name in memory:
                    memory[arr_name][idx] = val
                else:
                    raise Exception(f"Runtime Error: Array '{arr_name}' not defined.")

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
                if not executed_elif and stmt.else_body:
                    run_block(stmt.else_body)

        elif isinstance(stmt, While):
            while eval_expr(stmt.condition):
                run_block(stmt.body)

        elif isinstance(stmt, For):
            # 1. Run Init
            run_block([stmt.init])
            # 2. Loop while condition is true
            while eval_expr(stmt.condition):
                run_block(stmt.body)
                # 3. Run Update
                run_block([stmt.update])
        
        elif isinstance(stmt, ArrayAssign):
            idx = eval_expr(stmt.index)
            val = eval_expr(stmt.value)
            if stmt.name in memory:
                memory[stmt.name][idx] = val
            else:
                raise Exception(f"Runtime Error: Array '{stmt.name}' not defined.")

    # Main execution loop
    for stmt in ast:
        run(stmt)