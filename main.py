import sys

class PrePro:
    @staticmethod
    def filter(source):
        return '\n'.join(line.split('--')[0] for line in source.splitlines())

class SymbolTable:
    reserved_keywords = {'setup', 'and', 'or', 'not', 'if', 'else', 'repeat', 'do', 'end', 'then', 'var', 'function', 'return', 'chain', 'skipChain', 'singleCrochet', 'doubleCrochet', 'trebleCrochet', 'slipStitch', 'changeYarn', 'from', 'to'}
    
    def __init__(self):
        self.symbols = {}

    def get(self, name):
        if name not in self.symbols:
            raise ValueError(f"Variável não definida: {name}")
        return self.symbols[name]

    def create(self, name, value):
        if name in self.reserved_keywords:
            raise ValueError(f"Palavra reservada '{name}' não pode ser usada como identificador")
        elif name in self.symbols:
            raise ValueError(f"Variável já definida: {name}")
        self.symbols[name] = value

    def set(self, name, value):
        if name not in self.symbols:
            raise ValueError(f"Variável não definida: {name}")
        self.symbols[name] = value

    def remove(self, name):
        if name in self.symbols:
            del self.symbols[name]


class FuncTable:
    def __init__(self):
        self.functions = {}

    def get(self, key):
        if key not in self.functions:
            raise ValueError(f"Função não definida: {key}")
        return self.functions[key]
    
    def set(self, key, node):
        if key in self.functions:
            raise ValueError(f"Função já definida: {key}")
        self.functions[key] = node

class Node:
    def __init__(self):
        self.value = None
        self.children = []

    def evaluate(self, symbol_table):
        raise NotImplementedError
    

class Block(Node):
    def __init__(self):
        super().__init__()

    def evaluate(self, symbol_table):
        for child in self.children:
            child.evaluate(symbol_table)


class BinOp(Node):
    def __init__(self, left, right, operator):
        super().__init__()
        self.children = [left, right]
        self.operator = operator

    def evaluate(self, symbol_table):
        left_val = self.children[0].evaluate(symbol_table)
        right_val = self.children[1].evaluate(symbol_table)
        if self.operator == '+':
            if left_val[1] == "int" and right_val[1] == "int":
                return (left_val[0] + right_val[0], "int")
            else:
                raise ValueError("Operação inválida: soma só é permitida entre inteiros")
        elif self.operator == '-':
            if left_val[1] == "int" and right_val[1] == "int":
                return (left_val[0] - right_val[0], "int")
            else:
                raise ValueError("Operação inválida: subtração só é permitida entre inteiros")
        elif self.operator == '*':
            if left_val[1] == "int" and right_val[1] == "int":
                return (left_val[0] * right_val[0], "int")
            else:
                raise ValueError("Operação inválida: multiplicação só é permitida entre inteiros")
        elif self.operator == '/':
            if left_val[1] == "int" and right_val[1] == "int":
                if right_val[0] == 0:
                    raise ValueError("Divisão por zero")
                return (left_val[0] // right_val[0], "int")
            else:
                raise ValueError("Operação inválida: divisão só é permitida entre inteiros")
        elif self.operator == 'and':
            if left_val[1] == "int" and right_val[1] == "int":
                return (int(left_val[0] and right_val[0]), "int")
            else:
                raise ValueError("Operação inválida: 'and' só é permitida entre inteiros")
        elif self.operator == 'or':
            if left_val[1] == "int" and right_val[1] == "int":
                return (int(left_val[0] or right_val[0]), "int")
            else:
                raise ValueError("Operação inválida: 'or' só é permitida entre inteiros")
        elif self.operator == '==':
            if left_val[1] == right_val[1]:
                return (int(left_val[0] == right_val[0]), "int")
            else:
                raise ValueError("Operação inválida: operações relacionais só são permitidas entre valores do mesmo tipo")
        elif self.operator == '>':
            if left_val[1] == right_val[1]:
                return (int(left_val[0] > right_val[0]), "int")
            else:
                raise ValueError("Operação inválida: '>' só é permitido entre valores do mesmo tipo")
        elif self.operator == '<':
            if left_val[1] == right_val[1]:
                return (int(left_val[0] < right_val[0]), "int")
            else:
                raise ValueError("Operação inválida: '<' só é permitido entre valores do mesmo tipo")
        elif self.operator == '..':
            return (str(left_val[0]) + str(right_val[0]), "string")
        elif self.operator == '%':
            if left_val[1] == "int" and right_val[1] == "int":
                if right_val[0] == 0:
                    raise ValueError("Divisão por zero")
                return (left_val[0] % right_val[0], "int")
            else:
                raise ValueError("Operação inválida: módulo só é permitido entre inteiros")
        else:
            raise Exception("Operador desconhecido")

class UnOp(Node):
    def __init__(self, operand, operator):
        super().__init__()
        self.children = [operand]
        self.operator = operator

    def evaluate(self, symbol_table):
        operand_val = self.children[0].evaluate(symbol_table)
        if operand_val[1] != "int":
            raise ValueError("Operação inválida: operadores unários só são permitidos em inteiros")
        result = operand_val[0]
        for op in reversed(self.operator):  # Aplica cada operador na ordem correta
            if op == '+':
                result = +result
            elif op == '-':
                result = -result
            elif op == '!':
                result = not result
            else:
                raise Exception("Operador desconhecido")
        return (result, "int")

class IntVal(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def evaluate(self, symbol_table):
        return (self.value, "int")
    
class Identifier(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def evaluate(self, symbol_table):
        return symbol_table.get(self.value)

class Assign(Node):
    def __init__(self, identifier, expression):
        super().__init__()
        self.identifier = identifier
        self.expression = expression

    def evaluate(self, symbol_table):
        value = self.expression.evaluate(symbol_table)
        symbol_table.set(self.identifier.value, value)
        return value

class Repeat(Node):
    def __init__(self, identifier, start, end, block):
        super().__init__()
        self.identifier = identifier
        self.start = start
        self.end = end
        self.block = block
    
    def evaluate(self, symbol_table):
        start = self.start.evaluate(symbol_table)[0]
        end = self.end.evaluate(symbol_table)[0]
        for i in range(start, end + 1):
            self.block.evaluate(symbol_table)

class If(Node):
    def __init__(self, condition, if_block, else_block):
        super().__init__()
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block
    
    def evaluate(self, symbol_table):
        if self.condition.evaluate(symbol_table)[0]:
            self.if_block.evaluate(symbol_table)
        else:
            self.else_block.evaluate(symbol_table)

class NoOp(Node):
    def evaluate(self, symbol_table):
        return 0
    
class StringVal(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def evaluate(self, symbol_table):
        return (self.value, "string")
    
class VarDec(Node):
    def __init__(self, identifier, expression):
        super().__init__()
        self.identifier = identifier
        self.expression = expression

    def evaluate(self, symbol_table):
        if self.expression is not None:
            value = self.expression.evaluate(symbol_table)
        else:
            value = None
        symbol_table.create(self.identifier.value, value)
        return value
    
class FuncDec(Node):
    def __init__(self, identifier, params, block):
        super().__init__()
        self.identifier = identifier
        self.params = params
        self.block = block
    
    def evaluate(self, symbol_table):
        symbol_table.create(self.identifier.value, self)
        return self

class FuncCall(Node):
    def __init__(self, identifier, args):
        super().__init__()
        self.identifier = identifier
        self.args = args
    
    def evaluate(self, symbol_table):
        func = symbol_table.get(self.identifier)
        if not isinstance(func, FuncDec):
            raise ValueError(f"'{self.identifier}' não é uma função")
        if len(func.params) != len(self.args):
            raise ValueError(f"Quantidade de argumentos incorreta: esperado {len(func.params)}, mas obteve {len(self.args)}")
        local_table = SymbolTable()
        for i in range(len(self.args)):
            local_table.create(func.params[i].value, self.args[i].evaluate(symbol_table))
        # Copiando as variáveis globais para a tabela local
        for key, value in symbol_table.symbols.items():
            if key not in local_table.symbols:
                local_table.symbols[key] = value
        result = func.block.evaluate(local_table)
        # Atualizando as variáveis globais com a tabela local após execução
        for key, value in local_table.symbols.items():
            if key in symbol_table.symbols:
                symbol_table.set(key, value)
        return result

class Chain(Node):
    def __init__(self, count):
        super().__init__()
        self.count = count
    
    def evaluate(self, symbol_table):
        color = symbol_table.get("yarnColor")[0]
        color_code = get_color_code(color)
        print(f"{color_code}{'C' * self.count}\u001b[0m", end="")

class SkipChain(Node):
    def __init__(self, count):
        super().__init__()
        self.count = count
    
    def evaluate(self, symbol_table):
        print(f"{'-' * self.count}", end="")

class SingleCrochet(Node):
    def __init__(self, count):
        super().__init__()
        self.count = count
    
    def evaluate(self, symbol_table):
        color = symbol_table.get("yarnColor")[0]
        color_code = get_color_code(color)
        print(f"{color_code}{'S' * self.count}\u001b[0m", end="")

class DoubleCrochet(Node):
    def __init__(self, count):
        super().__init__()
        self.count = count
    
    def evaluate(self, symbol_table):
        color = symbol_table.get("yarnColor")[0]
        color_code = get_color_code(color)
        print(f"{color_code}{'D' * self.count}\u001b[0m", end="")

class TrebleCrochet(Node):
    def __init__(self, count):
        super().__init__()
        self.count = count
    
    def evaluate(self, symbol_table):
        color = symbol_table.get("yarnColor")[0]
        color_code = get_color_code(color)
        print(f"{color_code}{'T' * self.count}\u001b[0m", end="")

class SlipStitch(Node):
    def __init__(self, count):
        super().__init__()
        self.count = count
    
    def evaluate(self, symbol_table):
        color = symbol_table.get("yarnColor")[0]
        color_code = get_color_code(color)
        print(f"{color_code}{'L' * self.count}\u001b[0m", end="")

class ChangeYarn(Node):
    def __init__(self, yarn_color):
        super().__init__()
        self.yarn_color = yarn_color
    
    def evaluate(self, symbol_table):
        symbol_table.set("yarnColor", (self.yarn_color, "string"))

class TurnWork(Node):
    def __init__(self):
        super().__init__()

    def evaluate(self, symbol_table):
        print("\n", end="")

def get_color_code(yarn_color):
    colors = {
        "black": "\u001b[30m",
        "red": "\u001b[31m",
        "green": "\u001b[32m",
        "yellow": "\u001b[33m",
        "blue": "\u001b[34m",
        "magenta": "\u001b[35m",
        "cyan": "\u001b[36m",
        "white": "\u001b[37m",
        "gray": "\u001b[90m",
        # Add other colors as needed
    }
    return colors.get(yarn_color, "\u001b[37m")  # Default to white if color not found

        
        
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token(type={self.type}, value={self.value})"
    
class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.select_next()

    def select_next(self):
        while self.position < len(self.source) and self.source[self.position].isspace() and self.source[self.position] != '\n':
            self.position += 1

        if self.position == len(self.source):
            self.next = Token("EOF", "")
            return

        c = self.source[self.position]
        if c.isdigit():
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self.position += 1
            self.next = Token("INT", int(self.source[start:self.position]))
        elif c.isalpha() or c == '_':
            start = self.position
            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == '_'):
                self.position += 1
            value = self.source[start:self.position]
            keywords = {
                'setup': 'SETUP',
                'hookSize': 'HOOK_SIZE',
                'yarnColor': 'YARN_COLOR',
                'read': 'READ',
                'and': 'AND',
                'or': 'OR',
                'not': 'NOT',
                'if': 'IF',
                'else': 'ELSE',
                'repeat': 'REPEAT',
                'do': 'DO',
                'end': 'END',
                'then': 'THEN',
                'var': 'VAR',
                'function': 'FUNCTION',
                'return': 'RETURN',
                'chain': 'CHAIN',
                'skipChain': 'SKIP_CHAIN',
                'singleCrochet': 'SINGLE_CROCHET',
                'doubleCrochet': 'DOUBLE_CROCHET',
                'trebleCrochet': 'TREBLE_CROCHET',
                'slipStitch': 'SLIP_STITCH',
                'changeYarn': 'CHANGE_YARN',
                'turnWork': 'TURN_WORK',
                'from': 'FROM',
                'to': 'TO',
                'times': 'TIMES'
            }
            if value in keywords:
                self.next = Token(keywords[value], value)
            else:
                self.next = Token("IDENTIFIER", value)
        elif c == '+':
            self.next = Token("PLUS", c)
            self.position += 1
        elif c == '-':
            self.next = Token("MINUS", c)
            self.position += 1
        elif c == '*':
            self.next = Token("MULT", c)
            self.position += 1
        elif c == '%':
            self.next = Token("MOD", c)
            self.position += 1
        elif c == '/':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '/':
                self.position += 2
                while self.position < len(self.source) and self.source[self.position] != '\n':
                    self.position += 1
                self.select_next()
            else:
                self.next = Token("DIV", c)
                self.position += 1
        elif c == '(':
            self.next = Token("OPEN_PAR", c)
            self.position += 1
        elif c == ')':
            self.next = Token("CLOSE_PAR", c)
            self.position += 1
        elif c == '{':
            self.next = Token("OPEN_BRACE", c)
            self.position += 1
        elif c == '}':
            self.next = Token("CLOSE_BRACE", c)
            self.position += 1
        elif c == '=':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.next = Token("EQUALS", '==')
                self.position += 2
            else:
                self.next = Token("EQUAL", c)
                self.position += 1
        elif c == '<':
            self.next = Token("LESS_THAN", c)
            self.position += 1
        elif c == '>':
            self.next = Token("GREATER_THAN", c)
            self.position += 1
        elif c == '\n':
            self.next = Token("NEW_LINE", c)
            self.position += 1
        elif c == ',':
            self.next = Token("COMMA", c)
            self.position += 1
        elif c == ';':
            self.next = Token("SEMICOLON", c)
            self.position += 1
        elif c == '.':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '.':
                self.next = Token("CONCAT", '..')
                self.position += 2
        elif c == '"':
            start = self.position + 1
            self.position += 1
            while self.position < len(self.source) and self.source[self.position] != '"':
                self.position += 1
            if self.position == len(self.source):
                raise ValueError("Erro de sintaxe: aspas de fechamento não encontradas")
            value = self.source[start:self.position]
            self.next = Token("STRING", value)
            self.position += 1
        else:
            raise ValueError(f"Caractere inesperado: {c}") 

class Parser:
    
    @staticmethod
    def parse_setup(tokenizer):
        if tokenizer.next.type != "SETUP":
            raise ValueError("Erro de sintaxe: 'setup' esperado")
        tokenizer.select_next()
        if tokenizer.next.type != "OPEN_BRACE":
            raise ValueError("Erro de sintaxe: '{' esperado após 'setup'")
        tokenizer.select_next()
        if tokenizer.next.type != "NEW_LINE":
            raise ValueError("Nova linha esperada após '{'")
        tokenizer.select_next()
        while tokenizer.next.type != "CLOSE_BRACE":
            if tokenizer.next.type == "YARN_COLOR":
                tokenizer.select_next()
                if tokenizer.next.type != "EQUAL":
                    raise ValueError("Erro de sintaxe: '=' esperado após 'yarnColor'")
                tokenizer.select_next()
                if tokenizer.next.type != "STRING":
                    raise ValueError("Erro de sintaxe: string esperada após '='")
                yarn_color = tokenizer.next.value
                tokenizer.select_next()
                if tokenizer.next.type != "SEMICOLON":
                    raise ValueError("Erro de sintaxe: ';' esperado após string")
                tokenizer.select_next()
            elif tokenizer.next.type == "HOOK_SIZE":
                tokenizer.select_next()
                if tokenizer.next.type != "EQUAL":
                    raise ValueError("Erro de sintaxe: '=' esperado após 'hookSize'")
                tokenizer.select_next()
                if tokenizer.next.type != "INT":
                    raise ValueError("Erro de sintaxe: número esperado após '='")
                hook_size = tokenizer.next.value
                tokenizer.select_next()
                if tokenizer.next.type != "SEMICOLON":
                    raise ValueError("Erro de sintaxe: ';' esperado após número")
                tokenizer.select_next()
            elif tokenizer.next.type == "NEW_LINE":
                tokenizer.select_next()
            else:
                raise ValueError(f"Erro de sintaxe: identificador inválido: {tokenizer.next.type}")
        tokenizer.select_next()
        if yarn_color is None or hook_size is None:
            raise ValueError("Erro de sintaxe: 'yarnColor' e 'hookSize' são obrigatórios no bloco de configuração")
        if tokenizer.next.type != "SEMICOLON":
            raise ValueError("Erro de sintaxe: ';' esperado após '}'")
        tokenizer.select_next()
        return yarn_color, hook_size
    


    def parse_program(self, tokenizer, symbol_table):
        while tokenizer.next.type == "NEW_LINE":
            tokenizer.select_next()
        yarn_color, hook_size = Parser.parse_setup(tokenizer)
        symbol_table.create("yarnColor", (yarn_color, "string"))
        symbol_table.create("hookSize", (hook_size, "int"))
        block = Parser.parse_block(tokenizer, symbol_table)
        return block

    @staticmethod
    def parse_term(tokenizer):
        node = Parser.parse_factor(tokenizer)

        while tokenizer.next.type in ["MULT", "DIV", "MOD"]:
            if tokenizer.next.type == "MULT":
                tokenizer.select_next()
                node = BinOp(node, Parser.parse_factor(tokenizer), '*')
            elif tokenizer.next.type == "DIV":
                tokenizer.select_next()
                node = BinOp(node, Parser.parse_factor(tokenizer), '/')
            elif tokenizer.next.type == "MOD":
                tokenizer.select_next()
                node = BinOp(node, Parser.parse_factor(tokenizer), '%')
        return node
    
    @staticmethod
    def parse_factor(tokenizer):
        if tokenizer.next.type == "INT":
            value = tokenizer.next.value
            tokenizer.select_next()
            return IntVal(value)
        elif tokenizer.next.type == "STRING":
            value = tokenizer.next.value
            tokenizer.select_next()
            return StringVal(value)
        elif tokenizer.next.type == "IDENTIFIER":
            identifier = tokenizer.next.value
            tokenizer.select_next()
            # Verifica se o próximo token é uma abertura de parêntese para determinar se é uma chamada de função
            if tokenizer.next.type == "OPEN_PAR":
                tokenizer.select_next()  # Consome o token '('
                args = []
                if tokenizer.next.type != "CLOSE_PAR":
                    args.append(Parser.parse_b_expression(tokenizer))
                    while tokenizer.next.type == "COMMA":
                        tokenizer.select_next()  # Consome a vírgula
                        args.append(Parser.parse_b_expression(tokenizer))
                if tokenizer.next.type != "CLOSE_PAR":
                    raise ValueError("Erro de sintaxe: ')' esperado")
                tokenizer.select_next()
                if tokenizer.next.type != "SEMICOLON":
                    raise ValueError("Erro de sintaxe: ';' esperado após chamada de função")
                tokenizer.select_next()
                return FuncCall(identifier, args)
            return Identifier(identifier)
        elif tokenizer.next.type in ["PLUS", "MINUS", "NOT"]:
            operators = ""
            while tokenizer.next.type in ["PLUS", "MINUS", "NOT"]:
                operators += tokenizer.next.value
                tokenizer.select_next()
            factor = Parser.parse_factor(tokenizer)
            return UnOp(factor, operators)
        elif tokenizer.next.type == "OPEN_PAR":
            tokenizer.select_next()
            expression = Parser.parse_b_expression(tokenizer)
            if tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("Erro de sintaxe: ')' esperado")
            tokenizer.select_next()
            return expression
        else:
            raise ValueError(f"Erro de sintaxe: número, identificador ou '(' esperado, mas obteve '{tokenizer.next.type}'")

    @staticmethod
    def parse_expression(tokenizer):
        node = Parser.parse_term(tokenizer)

        while tokenizer.next.type in ["PLUS", "MINUS", "CONCAT"]:
            if tokenizer.next.type == "PLUS":
                tokenizer.select_next()
                node = BinOp(node, Parser.parse_term(tokenizer), '+')
            elif tokenizer.next.type == "MINUS":
                tokenizer.select_next()
                node = BinOp(node, Parser.parse_term(tokenizer), '-')
            elif tokenizer.next.type == "CONCAT":
                tokenizer.select_next()
                node = BinOp(node, Parser.parse_term(tokenizer), '..')
        return node

    @staticmethod
    def parse_rel_expression(tokenizer):
        node = Parser.parse_expression(tokenizer)

        if tokenizer.next.type in ["EQUALS", "LESS_THAN", "GREATER_THAN"]:
            operator = tokenizer.next.value
            tokenizer.select_next()
            return BinOp(node, Parser.parse_expression(tokenizer), operator)
        
        return node
    
    @staticmethod
    def parse_b_term(tokenizer):
        node = Parser.parse_rel_expression(tokenizer)

        while tokenizer.next.type == "AND":
            tokenizer.select_next()
            node = BinOp(node, Parser.parse_rel_expression(tokenizer), 'and')
        
        return node
    
    @staticmethod
    def parse_b_expression(tokenizer):
        node = Parser.parse_b_term(tokenizer)

        while tokenizer.next.type == "OR":
            tokenizer.select_next()
            node = BinOp(node, Parser.parse_b_term(tokenizer), 'or')
        
        return node

    @staticmethod
    def parse_block(tokenizer, symbol_table, inside_loop_or_conditional=False):
        block = Block()
        while tokenizer.next.type != "EOF":
            if tokenizer.next.type == "CLOSE_BRACE":
                if not inside_loop_or_conditional:
                    raise ValueError("Instrução 'end' fora de contexto")
                else:
                    return block
            if tokenizer.next.type == "ELSE":
                if not inside_loop_or_conditional:
                    raise ValueError("Instrução 'else' fora de contexto")
                else:
                    return block
            statement = Parser.parse_statement(tokenizer, symbol_table)
            if statement is not None:
                block.children.append(statement)
        return block


    def parse_statement(tokenizer, symbol_table):
        if tokenizer.next.type == "IDENTIFIER":
            identifier = Identifier(tokenizer.next.value)
            tokenizer.select_next()
            if tokenizer.next.type == "EQUAL":
                tokenizer.select_next()
                expression = Parser.parse_b_expression(tokenizer)
                if tokenizer.next.type != "SEMICOLON":
                    raise ValueError("Erro de sintaxe: ';' esperado após assign")
                tokenizer.select_next()
                return Assign(identifier, expression)
            elif tokenizer.next.type == "OPEN_PAR":
                tokenizer.select_next()
                args = []
                if tokenizer.next.type != "CLOSE_PAR":
                    args.append(Parser.parse_b_expression(tokenizer))
                    while tokenizer.next.type == "COMMA":
                        tokenizer.select_next()
                        args.append(Parser.parse_b_expression(tokenizer))
                if tokenizer.next.type != "CLOSE_PAR":
                    raise ValueError("Erro de sintaxe: ')' esperado")
                tokenizer.select_next()
                if tokenizer.next.type != "SEMICOLON":
                    raise ValueError("Erro de sintaxe: ';' esperado após chamada de função")
                tokenizer.select_next()
                return FuncCall(identifier.value, args)
            else:
                raise ValueError("Erro de sintaxe: '=' ou '(' esperado após identificador")
    

        elif tokenizer.next.type == "VAR":
            tokenizer.select_next()
            if tokenizer.next.type != "IDENTIFIER":
                raise ValueError("Identificador esperado após 'var'")
            identifier = Identifier(tokenizer.next.value)
            tokenizer.select_next()
            expression = None
            if tokenizer.next.type == "EQUAL":
                tokenizer.select_next()
                expression = Parser.parse_b_expression(tokenizer)
            if tokenizer.next.type != "SEMICOLON":
                raise ValueError("';' esperado após declaração de variável")
            tokenizer.select_next()
            return VarDec(identifier, expression)

        elif tokenizer.next.type == "IF":
            tokenizer.select_next()  # Consome o token 'IF'
            condition = Parser.parse_b_expression(tokenizer)
            if tokenizer.next.type != "OPEN_BRACE":
                raise ValueError("'{' esperado após a condição")
            tokenizer.select_next()  # Consome o token 'THEN'
            if tokenizer.next.type == "NEW_LINE":
                tokenizer.select_next()
            else:
                raise ValueError("Nova linha esperada após 'then'")
            if_block = Parser.parse_block(tokenizer, symbol_table, True)
            if tokenizer.next.type != "CLOSE_BRACE":
                raise ValueError("'}' esperado após o bloco")
            tokenizer.select_next()
            else_block = None
            if tokenizer.next.type == "ELSE":
                tokenizer.select_next()  # Consome o token 'ELSE'
                if tokenizer.next.type != "OPEN_BRACE":
                    raise ValueError("'{' esperado após 'else'")
                tokenizer.select_next()
                if tokenizer.next.type != "NEW_LINE":
                    raise ValueError("Nova linha esperada após 'else'")
                tokenizer.select_next()
                else_block = Parser.parse_block(tokenizer, symbol_table, True)
            if tokenizer.next.type != "CLOSE_BRACE":
                raise ValueError("'}' esperado após o bloco")
            tokenizer.select_next()
            if tokenizer.next.type != "NEW_LINE" and tokenizer.next.type != "EOF":
                raise ValueError("Nova linha esperada após o bloco")
            return If(condition, if_block, else_block)
        elif tokenizer.next.type == "REPEAT":
            tokenizer.select_next()
            if tokenizer.next.type != "IDENTIFIER":
                raise ValueError("Identificador esperado após 'repeat'")
            identifier = tokenizer.next.value
            tokenizer.select_next()
            if tokenizer.next.type != "FROM":
                raise ValueError("'from' esperado após o identificador")
            tokenizer.select_next()
            start = Parser.parse_b_expression(tokenizer)
            if tokenizer.next.type != "TO":
                raise ValueError("'to' esperado após o início do intervalo")
            tokenizer.select_next()
            end = Parser.parse_b_expression(tokenizer)
            if tokenizer.next.type != "OPEN_BRACE":
                raise ValueError("'{' esperado após o intervalo")
            tokenizer.select_next()
            if tokenizer.next.type != "NEW_LINE":
                raise ValueError("Nova linha esperada após '{'")
            tokenizer.select_next()
            block = Parser.parse_block(tokenizer, symbol_table, True)
            if tokenizer.next.type != "CLOSE_BRACE":
                raise ValueError("'}' esperado após o bloco")
            tokenizer.select_next()
            return Repeat(identifier, start, end, block)
        elif tokenizer.next.type == "ELSE":
            raise ValueError("Instrução 'else' fora de contexto")   
        elif tokenizer.next.type == "NEW_LINE":
            tokenizer.select_next()
            return NoOp()   
        elif tokenizer.next.type == "FUNCTION":
            tokenizer.select_next()
            if tokenizer.next.type != "IDENTIFIER":
                raise ValueError("Identificador esperado após 'function'")
            identifier = Identifier(tokenizer.next.value)
            tokenizer.select_next()
            if tokenizer.next.type != "OPEN_PAR":
                raise ValueError("'(' esperado após o identificador da função")
            tokenizer.select_next()
            params = []
            while tokenizer.next.type != "CLOSE_PAR":
                if tokenizer.next.type != "IDENTIFIER":
                    raise ValueError("Identificador esperado na lista de parâmetros")
                params.append(Identifier(tokenizer.next.value))
                tokenizer.select_next()
                if tokenizer.next.type == "COMMA":
                    tokenizer.select_next()
            tokenizer.select_next()
            if tokenizer.next.type != "OPEN_BRACE":
                raise ValueError("'{' esperado após a lista de parâmetros")
            tokenizer.select_next()
            if tokenizer.next.type != "NEW_LINE":
                raise ValueError("Nova linha esperada após a lista de parâmetros")
            tokenizer.select_next()
            block = Parser.parse_block(tokenizer, symbol_table, True)
            if tokenizer.next.type != "CLOSE_BRACE":
                raise ValueError("'}' esperado após o bloco da função")
            tokenizer.select_next()
            if tokenizer.next.type != "SEMICOLON":
                raise ValueError("';' esperado após a função")
            tokenizer.select_next()
            return FuncDec(identifier, params, block)
        elif tokenizer.next.type == "CHAIN":
            tokenizer.select_next()
            if tokenizer.next.type != "OPEN_PAR":
                raise ValueError("'(' esperado após 'chain'")
            tokenizer.select_next()
            if tokenizer.next.type != "INT":
                raise ValueError("Número esperado após '('")
            count = tokenizer.next.value
            tokenizer.select_next()
            if tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("')' esperado após o número")
            tokenizer.select_next()
            if tokenizer.next.type != "SEMICOLON":
                raise ValueError("';' esperado após a instrução")
            tokenizer.select_next()
            return Chain(count)
        elif tokenizer.next.type == "SKIP_CHAIN":
            tokenizer.select_next()
            if tokenizer.next.type != "OPEN_PAR":
                raise ValueError("'(' esperado após 'skipChain'")
            tokenizer.select_next()
            if tokenizer.next.type != "INT":
                raise ValueError("Número esperado após '('")
            count = tokenizer.next.value
            tokenizer.select_next()
            if tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("')' esperado após o número")
            tokenizer.select_next()
            if tokenizer.next.type != "SEMICOLON":
                raise ValueError("';' esperado após a instrução")
            tokenizer.select_next()
            return SkipChain(count)
        elif tokenizer.next.type == "SINGLE_CROCHET":
            tokenizer.select_next()
            if tokenizer.next.type != "OPEN_PAR":
                raise ValueError("'(' esperado após 'singleCrochet'")
            tokenizer.select_next()
            if tokenizer.next.type != "INT":
                raise ValueError("Número esperado após '('")
            count = tokenizer.next.value
            tokenizer.select_next()
            if tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("')' esperado após o número")
            tokenizer.select_next()
            if tokenizer.next.type != "SEMICOLON":
                raise ValueError("';' esperado após a instrução")
            tokenizer.select_next()
            return SingleCrochet(count)
        elif tokenizer.next.type == "DOUBLE_CROCHET":
            tokenizer.select_next()
            if tokenizer.next.type != "OPEN_PAR":
                raise ValueError("'(' esperado após 'doubleCrochet'")
            tokenizer.select_next()
            if tokenizer.next.type != "INT":
                raise ValueError("Número esperado após '('")
            count = tokenizer.next.value
            tokenizer.select_next()
            if tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("')' esperado após o número")
            tokenizer.select_next()
            if tokenizer.next.type != "SEMICOLON":
                raise ValueError("';' esperado após a instrução")
            tokenizer.select_next()
            return DoubleCrochet(count)
        elif tokenizer.next.type == "TREBLE_CROCHET":
            tokenizer.select_next()
            if tokenizer.next.type != "OPEN_PAR":
                raise ValueError("'(' esperado após 'trebleCrochet'")
            tokenizer.select_next()
            if tokenizer.next.type != "INT":
                raise ValueError("Número esperado após '('")
            count = tokenizer.next.value
            tokenizer.select_next()
            if tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("')' esperado após o número")
            tokenizer.select_next()
            if tokenizer.next.type != "SEMICOLON":
                raise ValueError("';' esperado após a instrução")
            tokenizer.select_next()
            return TrebleCrochet(count)
        elif tokenizer.next.type == "SLIP_STITCH":
            tokenizer.select_next()
            if tokenizer.next.type != "OPEN_PAR":
                raise ValueError("'(' esperado após 'slipStitch'")
            tokenizer.select_next()
            if tokenizer.next.type != "INT":
                raise ValueError("Número esperado após '('")
            count = tokenizer.next.value
            tokenizer.select_next()
            if tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("')' esperado após o número")
            tokenizer.select_next()
            if tokenizer.next.type != "SEMICOLON":
                raise ValueError("';' esperado após a instrução")
            tokenizer.select_next()
            return SlipStitch(count)
        elif tokenizer.next.type == "CHANGE_YARN":
            tokenizer.select_next()
            if tokenizer.next.type != "OPEN_PAR":
                raise ValueError("'(' esperado após 'changeYarn'")
            tokenizer.select_next()
            if tokenizer.next.type != "STRING":
                raise ValueError("String esperada após '('")
            color = tokenizer.next.value
            tokenizer.select_next()
            if tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("')' esperado após a string")
            tokenizer.select_next()
            if tokenizer.next.type != "SEMICOLON":
                raise ValueError("';' esperado após a instrução")
            tokenizer.select_next()
            return ChangeYarn(color)
        elif tokenizer.next.type == "TURN_WORK":
            tokenizer.select_next()
            if tokenizer.next.type != "OPEN_PAR":
                raise ValueError("'(' esperado após 'turnWork'")
            tokenizer.select_next()
            if tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("')' esperado após '('")
            tokenizer.select_next()
            if tokenizer.next.type != "SEMICOLON":
                raise ValueError("';' esperado após a instrução")
            tokenizer.select_next()
            return TurnWork()

        else:
            raise ValueError("Instrução não reconhecida: " + tokenizer.next.type)
        

    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        tokenizer = Tokenizer(code)
        symbol_table = SymbolTable()
        parser = Parser()
        block = parser.parse_program(tokenizer, symbol_table)
        block.evaluate(symbol_table)        
        return symbol_table

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Por favor, forneça o caminho para um arquivo .yn")
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                code = file.read()
            Parser.run(code)
        except ValueError as e:
            sys.stderr.write(str(e) + "\n")




