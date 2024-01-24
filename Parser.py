import re
import display 
from display import ParseTreePrinter


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type}: {self.value}" if self.value is not None else f"{self.type}"


class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.tokens = []

    def tokenize(self):
        while self.position < len(self.source_code):
            char = self.source_code[self.position]

            if char.isspace():
                self.consume_whitespace()
            elif char.isalpha():
                identifier = self.consume_while(lambda x: x.isalnum() or x == '_')
                token_type = self.get_keyword_or_id(identifier)
                self.tokens.append(Token(token_type, identifier))
            elif char.isdigit():
                integer_literal = self.consume_while(lambda x: x.isdigit())
                self.tokens.append(Token("INTEGER", int(integer_literal)))
            elif char == '{':
                self.tokens.append(Token("LBRACE"))
                self.position += 1
            elif char == '}':
                self.tokens.append(Token("RBRACE"))
                self.position += 1
            elif char == '(':
                self.tokens.append(Token("LPAREN"))
                self.position += 1
            elif char == ')':
                self.tokens.append(Token("RPAREN"))
                self.position += 1
            elif char == '.':
                self.tokens.append(Token("DOT"))
                self.position += 1
            elif char == '#':
                self.tokens.append(Token("HASH"))
                self.position += 1    
            elif char == ':':
                self.tokens.append(Token("COLON"))
                self.position += 1
            elif char == ',':
                self.tokens.append(Token("COMMA"))
                self.position += 1
            elif char == '+':
                self.tokens.append(Token("PLUS"))
                self.position += 1
            elif char == '-':
                self.tokens.append(Token("MINUS"))
                self.position += 1
            elif char == '*':
                self.tokens.append(Token("MULTIPLY"))
                self.position += 1
            elif char == '/':
                self.tokens.append(Token("DIVIDE"))
                self.position += 1
            elif char == ';':
                self.tokens.append(Token("SEMICOLON"))
                self.position += 1
            elif char == '<' and self.source_code[self.position + 1] == '-':
                self.tokens.append(Token("ASSIGN"))
                self.position += 2
            else:
                raise SyntaxError(f"Unexpected character: {char}")

        return self.tokens

    def consume_while(self, condition):
        result = ""
        while self.position < len(self.source_code) and condition(self.source_code[self.position]):
            result += self.source_code[self.position]
            self.position += 1
        return result
    
    def consume_whitespace(self):
        self.consume_while(lambda x: x.isspace())

    def get_keyword_or_id(self, identifier):
        keywords = {"class", "inherits", "if", "then", "else", "fi", "while", "loop", "pool", "let", "in", "case", "of", "esac", "new", "isvoid", "not"}
        return "KEYWORD" if identifier.lower() in keywords else "ID"


# Now integrate the Lexer with the Parser

class ASTNode:
    def __init__(self, node_type, attributes=None, children=None):
        self.node_type = node_type
        self.attributes = attributes if attributes else {}
        self.children = children if children else []

    def __repr__(self, level=0):
        ret = "\t" * level + f"{self.node_type}\n"
        for child in self.children:
            if isinstance(child, ASTNode):
                ret += child.__repr__(level + 1)
            elif isinstance(child, Token):
                ret += "\t" * (level + 1) + f"{child}\n"
            else:
                ret += "\t" * (level + 1) + f"{child}\n"
        return ret

    def display(self, level=0):
        indent = "\t" * level
        print(f"{indent}{self.node_type}")

        if isinstance(self.attributes, dict):
            for key, value in self.attributes.items():
                print(f"{indent}\t{key}: {value}")
        elif isinstance(self.attributes, list):
            for attribute in self.attributes:
                print(f"{indent}\t{attribute}")

        for child in self.children:
            if isinstance(child, ASTNode):
                child.display(level + 1)
            elif isinstance(child, Token):
                print(f"{indent}\t{child}")
            else:
                print(f"{indent}\t{child}")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.ast = None

    def parse(self):
        self.consume_token()
        self.ast = self.program()
        

    def match(self, expected_type):
        if self.current_token.type == expected_type:
            token = self.current_token
            self.consume_token()
            return token
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def consume_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
            print(f"Consumed token: {self.current_token}")          
        else:
            self.current_token = None

    def program(self):
        return ASTNode("Program", [self.class_list()])

    def class_list(self):
        classes = []
        while self.current_token and self.current_token.type == "CLASS":
            classes.append(self.class_declaration())
        return ASTNode("classDefine", classes)

    def class_declaration(self):
        self.match("CLASS")
        class_name = self.match("ID").value
        base_class = None

        if self.current_token and self.current_token.type == "INHERITS":
            self.consume_token()  # Consume "inherits"
            base_class = self.match("ID").value

        self.match("{")
        features = self.feature_list(class_name)
        self.match("}")

        return ASTNode("ClassDeclaration", attributes={"class_name": class_name, "base_class": base_class}, children=features)

    def feature(self):
        feature_name = self.match("ID").value
        if self.current_token and self.current_token.type == "(":
            return self.method(feature_name)
        else:
            return self.attribute(feature_name)

    def feature_list(self, class_name):
        features = []
        while self.current_token and self.current_token.type == "ID":
            features.append(self.feature())
            print(features)
        return features

        

    def method(self, method_name):
        self.match("(")
        parameters = self.formal_parameters()
        self.match(")")
        self.match(":")
        return_type = self.match("ID").value  # Assuming methods return type is an ID for simplicity
        self.match("{")
        body = self.expression()
        self.match("}")
        return ASTNode("Method", [method_name, parameters, return_type, body])

    def formal_parameters(self):
        params = []
        while self.current_token and self.current_token.type == "ID":
            param_name = self.match("ID").value
            self.match(":")
            param_type = self.match("TYPE").value
            params.append(ASTNode("FormalParameter", [param_name, param_type]))
            if self.current_token and self.current_token.type == ",":
                self.consume_token()  # Consume the comma
            else:
                break
        return ASTNode("FormalParameters", params)

    def attribute(self, attribute_name):
        self.match(":")
        attribute_type = self.match("TYPE").value
        if self.current_token and self.current_token.type == "<-":
            self.consume_token()  # Consume the "<-"
            initial_expr = self.expression()
        else:
            initial_expr = None
        return ASTNode("Attribute", [attribute_name, attribute_type, initial_expr])

    def expression(self):
        # Simplified expression parsing for demonstration purposes
        if self.current_token and self.current_token.type == "ID":
            return ASTNode("Identifier", [self.match("ID").value])
        elif self.current_token and self.current_token.type == "INTEGER":
            return ASTNode("IntegerLiteral", [self.match("INTEGER").value])
        else:
            raise SyntaxError("Unexpected token in expression")

# Example usage:
source_code = """
class Main inherits IO {
    main() : Object {
        let x : Int <- 5 + 3 in
            x + 2
    };
};
"""

'''
source_code = """
class Shape {
    area(): Int {
        0
    };
};

class Circle inherits Shape {
    radius: Int;

    init(r: Int): SELF_TYPE {
        {
            self.radius <- r;
            self
        }
    };

    area(): Int {
        3 * self.radius * self.radius
    };
};

class Main {
    main(): Object {
        let shape: Shape <- new Shape in
            out_int(shape.area()); # Output: 0

        let circle: Circle <- new Circle(5) in
            out_int(circle.area()); # Output: 75
    };
};
"""
'''

lexer = Lexer(source_code)
tokens = lexer.tokenize()
print("Tokens:")
for token in tokens:
    print(token)
parser = Parser(tokens)
parser.parse()
print("\nParse Tree:")
print(parser.ast.__repr__())

printer = ParseTreePrinter()
printer.print_tree(display.parse_tree1)
