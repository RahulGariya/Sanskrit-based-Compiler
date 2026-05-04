
# 🕉️ Sanskrit Compiler

A **mini compiler for a Sanskrit-based programming language**, built to demonstrate core concepts of **Compiler Design** including lexical analysis, parsing, intermediate code generation, and execution.

---

## 🚀 Features

* ✅ Sanskrit-based syntax (Devanagari keywords)
* ✅ Variables and arithmetic operations (`+ - * /`)
* ✅ Conditional statements (`यदि`, `अथ`)
* ✅ Loops (`किन्चित्काल`)
* ✅ String support (like `निर्गम "Hello"`)
* ✅ Block execution using `{ }`
* ✅ Intermediate Code Generation (Three Address Code - TAC)
* ✅ Target Code Generation (Pseudo Assembly)
* ✅ Execution Engine (Interpreter)

---

## 🧠 Compiler Phases Implemented

1. **Lexical Analysis**

   * Converts source code into tokens
   * Supports Unicode (Devanagari)

2. **Syntax Analysis**

   * Builds Abstract Syntax Tree (AST)

3. **Intermediate Code Generation**

   * Generates Three Address Code (TAC)

4. **Target Code Generation**

   * Produces pseudo assembly instructions

5. **Execution**

   * Interprets AST to produce actual output

---

## 📁 Project Structure

```
sanskrit-compiler/
│
├── main.py / sanskrit.py   # Entry point
├── lexer.py                # Tokenizer
├── parser.py               # Syntax analyzer
├── ast_nodes.py            # AST node definitions
├── tac.py                  # Intermediate code generation
├── codegen.py              # Target code generation
├── executor.py             # Execution engine
└── sample.skt              # Sample program
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone <your-repo-link>
cd sanskrit-compiler
```

### 2. Run the compiler

```
python3 main.py sample.skt
```

---

## 🧪 Example Programs

### 🔹 Basic Arithmetic

```
x = 5;
y = 3;
निर्गम x + y;
```

---

### 🔹 If-Else Example

```
x = 10;
y = 5;

यदि x > y तदा
{
    निर्गम "x is greater";
}
अथ
{
    निर्गम "y is greater";
};
```

---

### 🔹 While Loop Example

```
x = 5;

किन्चित्काल x > 0 तदा
{
    निर्गम x;
    x = x - 1;
};

निर्गम "done";
```

---

## 🖥️ Sample Output

```
--- TAC ---
t1 = x PLUS y
PRINT t1

--- TARGET CODE ---
LOAD x
STORE t1
PRINT t1

--- EXECUTION ---
8
```

---

## 🌐 Language Design

| Sanskrit Keyword | Meaning |
| ---------------- | ------- |
| यदि              | if      |
| तदा              | then    |
| अथ               | else    |
| किन्चित्काल      | while   |
| निर्गम           | print   |

---

## ⚠️ Notes

* Source files must be saved in **UTF-8 encoding**
* Devanagari Unicode is fully supported
* Recommended to use English variable names for simplicity

---

## 🎓 Academic Purpose

This project was built to demonstrate:

* Compiler construction fundamentals
* Language design using non-English syntax
* Handling Unicode in programming languages

---

## 💡 Future Improvements

* Function support
* Real assembly (MIPS) generation
* Optimization phase
* Error handling improvements

---



