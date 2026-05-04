from ast_nodes import Num, Var, BinOp, UnaryOp, Assign, Print, If, While

temp_count = 0
label_count = 0  # Added for control flow (IF/WHILE)

def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"

def new_label():
    global label_count
    label_count += 1
    return f"L{label_count}"

def generate_TAC(node, code):
    if isinstance(node, Num):
        return str(node.value)

    if isinstance(node, Var):
        return node.name

    # --- NEW: UNARY OPERATOR FOR 'NOT' ---
    if isinstance(node, UnaryOp):
        expr = generate_TAC(node.expr, code)
        temp = new_temp()
        code.append(f"{temp} = {node.op} {expr}")
        return temp

    # BinOp already automatically supports AND, OR, XOR 
    # because it dynamically reads node.op!
    if isinstance(node, BinOp):
        left = generate_TAC(node.left, code)
        right = generate_TAC(node.right, code)
        temp = new_temp()
        code.append(f"{temp} = {left} {node.op} {right}")
        return temp

    if isinstance(node, Assign):
        val = generate_TAC(node.value, code)
        code.append(f"{node.name} = {val}")

    if isinstance(node, Print):
        val = generate_TAC(node.value, code)
        code.append(f"PRINT {val}")

   
    
    if isinstance(node, If):
        l_end = new_label()
        
       
        cond = generate_TAC(node.condition, code)
        l_next = new_label()
        code.append(f"IF_FALSE {cond} GOTO {l_next}")
        
        for stmt in node.body: generate_TAC(stmt, code)
        code.append(f"GOTO {l_end}") # Jump to end if true
        
        
        code.append(f"{l_next}:")
        for elif_cond, elif_body in node.elifs:
            e_cond = generate_TAC(elif_cond, code)
            l_next = new_label()
            code.append(f"IF_FALSE {e_cond} GOTO {l_next}")
            
            for stmt in elif_body: generate_TAC(stmt, code)
            code.append(f"GOTO {l_end}") # Jump to end if true
            code.append(f"{l_next}:")
            
        
        for stmt in node.else_body: generate_TAC(stmt, code)
        
       
        code.append(f"{l_end}:")
 
    if isinstance(node, While):
        l_start = new_label()
        l_end = new_label()
        
       
        code.append(f"{l_start}:")
        
        cond = generate_TAC(node.condition, code)
        code.append(f"IF_FALSE {cond} GOTO {l_end}")
        
   
       
        for stmt in node.body:
            generate_TAC(stmt, code)
            
      
        code.append(f"GOTO {l_start}")
        
        
        code.append(f"{l_end}:")