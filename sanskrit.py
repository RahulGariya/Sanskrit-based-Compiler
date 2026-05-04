#!/usr/bin/env python3

import sys
from lexer import tokenize
from parser import Parser
from tac import generate_TAC
from codegen import generate_target
from executor import execute

if len(sys.argv) < 2:
    print("Usage: sanskrit <file.skt>")
    sys.exit(1)

filename = sys.argv[1]

code = open(filename, encoding="utf-8").read()

tokens = tokenize(code)
parser = Parser(tokens)
ast = parser.parse()

tac = []
for stmt in ast:
    generate_TAC(stmt, tac)

#print("\n--- TAC ---")
#for line in tac:
#   print(line)
asm_code = generate_target(tac)

with open("output.asm", "w") as f:
    for line in asm_code:
        f.write(line + "\n")

print("Assembly file generated: output.asm")

#print("\n--- EXECUTION ---")
execute(ast)
