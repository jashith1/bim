from bim_token import *
from ast_nodes import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type):
        """Move forward if everything is correct"""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token.type}")
        
    def skip_newlines(self):
        """Skip any newline tokens"""
        while self.current_token.type == TokenType.NEWLINE:
            self.eat(TokenType.NEWLINE)

    
    def factor(self):
        """Higher priority (numbers, paranthesis, strings, functions, etc)"""
        token = self.current_token
        
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            return UnaryOpNode(token, self.factor()) 
        
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return UnaryOpNode(token, self.factor())

        elif token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberNode(float(token.value))
        
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return StringNode(token.value)
        
        elif token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return BooleanNode(True)
        
        elif token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return BooleanNode(False)
        
        elif token.type == TokenType.IDENTIFIER:
            function_name = token.value
            self.eat(TokenType.IDENTIFIER)
            
            if self.current_token.type == TokenType.LPAREN:
                #function call
                self.eat(TokenType.LPAREN)
                arguments = self.parse_arguments()
                self.eat(TokenType.RPAREN)
                return FunctionCallNode(function_name, arguments)
            else:
                #just a variable
                return VariableNode(function_name)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression() 
            self.eat(TokenType.RPAREN) 
            return node

        
        raise Exception(f"Unexpected token: {token.type}")
    
    def term(self):
        """parse and return AST for multiplication and division (medium-high priority in PEMDAS)"""
        node = self.factor()
        
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            
            node = BinaryOpNode(left=node, operator=token, right=self.factor())
        
        return node
    
    def arithmetic_expression(self):
        """Parse and return AST for addition and subtraction (medium-low priority in PEMDAS)"""
        node = self.term()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinaryOpNode(left=node, operator=token, right=self.term())
        
        return node
    
    def expression(self):
        """Lowest precedence: comparison operators"""
        node = self.arithmetic_expression()
        possible = (TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS_THAN, TokenType.GREATER_THAN, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL)
        
        while self.current_token.type in possible:
            token = self.current_token
            if token.type == TokenType.EQUAL:
                self.eat(TokenType.EQUAL)
            elif token.type == TokenType.NOT_EQUAL:
                self.eat(TokenType.NOT_EQUAL)
            elif token.type == TokenType.LESS_THAN:
                self.eat(TokenType.LESS_THAN)
            elif token.type == TokenType.GREATER_THAN:
                self.eat(TokenType.GREATER_THAN)
            elif token.type == TokenType.LESS_EQUAL:
                self.eat(TokenType.LESS_EQUAL)
            elif token.type == TokenType.GREATER_EQUAL:
                self.eat(TokenType.GREATER_EQUAL)
            
            node = BinaryOpNode(left=node, operator=token, right=self.arithmetic_expression())
        
        return node
    
    def statement(self):
        """Parse a statement (ie assignment or expression)"""
        self.skip_newlines()
        if self.current_token.type == TokenType.IF:
            return self.parse_if()
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while()
        elif self.current_token.type == TokenType.FOR:
            return self.parse_for()


        if self.current_token.type == TokenType.IDENTIFIER:
            #temporarily store the data
            saved_lexer_pos = self.lexer.pos
            saved_lexer_char = self.lexer.current_char
            var_name = self.current_token.value
            
            self.eat(TokenType.IDENTIFIER)
            
            if self.current_token.type == TokenType.ASSIGN:
                self.eat(TokenType.ASSIGN)
                value = self.expression()
                return AssignmentNode(var_name, value)
            else:
                # Not an assignment, restore state and parse as expression
                self.lexer.pos = saved_lexer_pos
                self.lexer.current_char = saved_lexer_char
                self.current_token = Token(TokenType.IDENTIFIER, var_name)
        
        # Parse as expression
        return self.expression()
    
    def parse_arguments(self):
        """Parse comma separated function arguments"""
        arguments = []
        
        #empty
        if self.current_token.type == TokenType.RPAREN:
            return arguments
        
        #first
        arguments.append(self.expression())
        
        #the rest (comma separeted)
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            arguments.append(self.expression())
        
        return arguments

    def parse_block(self):
        """Parse a block of statements enclosed in braces"""
        self.eat(TokenType.LBRACE)        
        self.skip_newlines()
        statements = []
        
        while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
            stmt = self.statement()
            statements.append(stmt)
            
            while self.current_token.type in (TokenType.SEMICOLON, TokenType.COMMA, TokenType.NEWLINE):
                self.current_token = self.lexer.get_next_token()
        
        self.eat(TokenType.RBRACE)
        return BlockNode(statements)

    def parse_if(self):
        """Parse if statement"""
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.expression()
        self.eat(TokenType.RPAREN)
        
        self.skip_newlines()
        if_body = self.parse_block()

        elif_clauses = []
        self.skip_newlines()

        while self.current_token.type == TokenType.ELIF:
            self.eat(TokenType.ELIF)
            self.eat(TokenType.LPAREN)
            elif_condition = self.expression()
            self.eat(TokenType.RPAREN)
            
            self.skip_newlines()
            elif_body = self.parse_block()
            
            elif_clauses.append((elif_condition, elif_body))
            self.skip_newlines()
        
        else_body = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.skip_newlines()
            else_body = self.parse_block()
        
        return IfNode(condition, if_body, elif_clauses, else_body)
    
    def parse_while(self):
        """Parse while loop"""
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.expression()
        self.eat(TokenType.RPAREN)
        
        self.skip_newlines()
        body = self.parse_block()
        
        return WhileNode(condition, body)

    def parse_for(self):
        """Parse for loop"""
        self.eat(TokenType.FOR)
        self.eat(TokenType.LPAREN)
        
        if self.current_token.type != TokenType.IDENTIFIER:
            raise Exception("Expected variable name in for loop")
        variable_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.IN)
        iterable = self.expression()  # This could be range() or other iterable
        
        self.eat(TokenType.RPAREN)
        self.skip_newlines()
        body = self.parse_block()
        
        return ForNode(variable_name, iterable, body)

    
    def parse_program(self):
        """Parse complete program with multiple statements"""
        statements = []
        
        while self.current_token.type != TokenType.EOF:
            self.skip_newlines() 
            
            if self.current_token.type == TokenType.EOF:
                break
                
            stmt = self.statement()
            statements.append(stmt)
            
            while self.current_token.type in (TokenType.SEMICOLON, TokenType.COMMA, TokenType.NEWLINE):
                self.current_token = self.lexer.get_next_token()
        
        return BlockNode(statements)

