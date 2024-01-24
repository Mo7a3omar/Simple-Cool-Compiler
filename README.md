# Simple-Cool-Compiler

## Overview
This project implements a simple compiler for the Cool (Classroom Object Oriented Language) programming language. The compiler consists of a lexer and a parser that generate an Abstract Syntax Tree (AST) from Cool source code.

## Components

### 1. Lexer
The lexer tokenizes the input Cool source code, identifying different types of tokens such as keywords, identifiers, integers, and symbols. Each token is represented as an object of the `Token` class.

### 2. Parser
The parser takes the tokens generated by the lexer and constructs an Abstract Syntax Tree (AST) representing the structure of the Cool program. The AST is composed of nodes representing various constructs in the Cool language, such as class declarations, methods, attributes, expressions, etc.

### 3. ASTNode
The `ASTNode` class defines the nodes used in the AST. Each node has a type, attributes, and children. It provides methods for representation and display of the tree structure.

## Usage
1. **Install Python:**
   - Ensure you have Python installed on your system.

2. **Run the Compiler:**
   - Execute the provided code in a Python environment.
   - Modify the `source_code` variable with your Cool program.

3. **Review Output:**
   - View the generated tokens and the resulting AST.
   - Analyze the parse tree structure to understand the program's syntax.
