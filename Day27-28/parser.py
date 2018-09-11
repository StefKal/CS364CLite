import ast
import lexer


class Parser:

    def __init__(self, filename):

        lex = lexer.Lexer()
        self.tokens = lex.token_generator(filename)

        # currtok is the current token that we are looking at
        self.currtok = next(self.tokens)

    def parse(self):
        return self.program()

    # nested if/else in order to check for the correct syntax of main function
    # Grammar: "int" "main" "(" ")" "{" Declarations Statements "}"
    def program(self):
        if self.currtok[0] == "KWDINT":
            self.currtok = next(self.tokens)
            if self.currtok[0] == "KWDMAIN":
                self.currtok = next(self.tokens)
                if self.currtok[0] == "PCTLPAR":
                    self.currtok = next(self.tokens)
                    if self.currtok[0] == "PCTRPAR":
                        self.currtok = next(self.tokens)
                        if self.currtok[0] == "PCTLBRA":

                            self.currtok = next(self.tokens)

                            # follow grammatically correct syntax (declarations and statements)
                            d = self.decls()
                            s = self.statements()

                            # run the declarations and statements in the abstract syntax tree for program
                            if self.currtok[0] == "PCTRBRA":
                                return ast.Program(d, s)
                            else:
                                raise CLiteSyntaxError("Right brace expected", self.currtok[1])
                        else:
                            raise CLiteSyntaxError("Left brace expected", self.currtok[1])
                    else:
                        raise CLiteSyntaxError("Right parenthesis expected", self.currtok[1])
                else:
                    raise CLiteSyntaxError("Left parenthesis expected", self.currtok[1])
            else:
                raise CLiteSyntaxError("keyword main expected", self.currtok[1])
        else:
            raise CLiteSyntaxError("keyword int expected", self.currtok[1])

    # Grammar: Declarations => { Declaration }
    def decls(self):
        d = {}
        decls = []
        while self.currtok[0] == "KWDINT" or self.currtok[0] == "KWDBOOL" \
                or self.currtok[0] == "KWDFLOAT":
            decl = self.decl()
            if decl.name in d:
                raise CLiteSyntaxError("Value already declared", self.currtok[1])
            # create a dictionary with the name as key and the type as the value (eg. key: X value: INT)
            d[decl.name] = decl.type
            decls.append(str(decl))
        return ast.decls(decls)

    # Grammar: Declaration => Type Identifier ";"
    def decl(self):
        tmpType = self.currtok[2]
        self.type()

        if self.currtok[0] == "IDENTIFIER":
            tmpNAME = self.currtok[2]
            self.currtok = next(self.tokens)
            if self.currtok[0] == "PCTSEMI":
                self.currtok = next(self.tokens)
                return ast.decl(tmpNAME, tmpType)
            else:
                raise CLiteSyntaxError(" ';' expected", self.currtok[1])
        else:
            raise CLiteSyntaxError("IDENTIFIER expected", self.currtok[1])

    # Grammar: Statements => { Statement }
    def statements(self):
        s = []
        while self.currtok[0] == "PCTSEMI" or self.currtok[0] == "PCTLBRA" or \
                self.currtok[0] == "IDENTIFIER" or self.currtok[0] == "KWDIF" or \
                self.currtok[0] == "KWDWHILE" or self.currtok[0] == "KWDPRINT":
            stmt = self.statement()
            s.append(str(stmt))
        return ast.Stmts(s)

    # Grammar: Type => int | bool | float
    def type(self):
        if self.currtok[0] == 'KWDINT':
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            return tmpID
        elif self.currtok[0] == 'KWDBOOL':
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            return tmpID
        elif self.currtok[0] == 'KWDFLOAT':
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            return tmpID

    # Grammar: Statement => ";" | Block | Assignment | IfStatement | WhileStatement | PrintStatement
    def statement(self):
        if self.currtok[0] == "PCTSEMI":
            return ast.SemiStmt()
        elif self.currtok[0] == "PCTLBRA":
            ast.indent_level += 1
            return self.block()
        elif self.currtok[0] == "IDENTIFIER":
            return self.assignment()
        elif self.currtok[0] == "KWDIF":
            return self.if_statement()
        elif self.currtok[0] == "KWDWHILE":
            return self.while_statement()
        elif self.currtok[0] == "KWDPRINT":
            return self.print_statement()

    # Grammar: Block => "{" Statements "}"
    def block(self):
        if self.currtok[0] == "PCTLBRA":
            self.currtok = next(self.tokens)
            b = self.statements()
            if self.currtok[0] == "PCTRBRA":
                self.currtok = next(self.tokens)
                return ast.Block(b)
            else:
                raise CLiteSyntaxError("Right Brace expected", self.currtok[1])
        else:
            raise CLiteSyntaxError("Left brace expected", self.currtok[1])

    # Grammar: Assignment => Identifier = Expression ";"
    def assignment(self):
        if self.currtok[0] == "IDENTIFIER":
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            if self.currtok[0] == "ASSIGNMENT":
                self.currtok = next(self.tokens)
                expr = self.expression()
                if self.currtok[0] == "PCTSEMI":
                    self.currtok = next(self.tokens)
                    return ast.assignment(tmpID, expr)
                else:
                    raise CLiteSyntaxError(" ';' expected", self.currtok[1])
            else:
                raise CLiteSyntaxError(" '=' expected ", self.currtok[1])
        else:
            raise CLiteSyntaxError(" Missing Identifier", self.currtok[1])

    # Grammar: IfStatement => "if" "(" Expression ")" Statement [ "else" Statement ]
    def if_statement(self):

        if self.currtok[0] == "KWDIF":
            self.currtok = next(self.tokens)

            if self.currtok[0] == "PCTLPAR":
                self.currtok = next(self.tokens)
                cond = self.expression()

                if self.currtok[0] == "PCTRPAR":

                    self.currtok = next(self.tokens)
                    stmt = self.statement()

                    if self.currtok[0] == "KWDELSE":
                        self.currtok = next(self.tokens)
                        elsestmt = self.statement()
                        return ast.IfStmt(cond, stmt, elsestmt)
                    else:

                        return ast.IfStmt(cond, stmt)
                else:
                    raise CLiteSyntaxError("Right parenthesis expected", self.currtok[1])
            else:
                raise CLiteSyntaxError("Left parenthesis expected", self.currtok[1])
        else:
            raise CLiteSyntaxError("Keyword if expected", self.currtok[1])

    # Grammar: WhileStatement => "while" "(" Expression ")" Statement
    def while_statement(self):
        if self.currtok[0] == "KWDWHILE":
            self.currtok = next(self.tokens)
            if self.currtok[0] == "PCTLPAR":
                self.currtok = next(self.tokens)
                cond = self.expression()

                if self.currtok[0] == "PCTRPAR":
                    self.currtok = next(self.tokens)
                    stmt = self.statement()
                    ast.indent_level -= 1
                    return ast.WhileStmt(cond, stmt)

                else:
                    raise CLiteSyntaxError("Right parenthesis expected", self.currtok[1])
            else:
                raise CLiteSyntaxError("Left parenthesis expected", self.currtok[1])
        else:
            raise CLiteSyntaxError("While keyword expected", self.currtok[1])


    # Grammar: PrintStatement => "print" "(" Expression ")" ";"
    def print_statement(self):
        if self.currtok[0] == "KWDPRINT":
            self.currtok = next(self.tokens)
            if self.currtok[0] == "PCTLPAR":
                self.currtok = next(self.tokens)
                body = self.expression()

                if self.currtok[0] == "PCTRPAR":
                    self.currtok = next(self.tokens)

                    if self.currtok[0] == "PCTSEMI":
                        self.currtok = next(self.tokens)
                        ast.indent_level -= 1
                        return ast.PrintStmt(body)

                    else:
                        raise CLiteSyntaxError("Semicolon expected", self.currtok[1])
                else:
                    raise CLiteSyntaxError("Right parenthesis expected", self.currtok[1])
            else:
                raise CLiteSyntaxError("Left parenthesis expected", self.currtok[1])
        else:
            raise CLiteSyntaxError("print keyword expected", self.currtok[1])

    # Grammar: Expression => Conjunction { || Conjunction }
    def expression(self):
        left_tree = self.conjunction()

        while self.currtok[0] == 'OR':
            self.currtok = next(self.tokens)
            right_tree = self.conjunction()
            left_tree = ast.BinaryExpr(left_tree, right_tree, '||')

        return left_tree

    # Grammar: Conjunction => Equality { && Equality }
    def conjunction(self):

        left_tree = self.equality()

        while self.currtok[0] == 'AND':
            self.currtok = next(self.tokens)
            right_tree = self.equality()
            left_tree = ast.BinaryExpr(left_tree, right_tree, '&&')

        return left_tree

    # Grammar: Equality => Relation [ EqOperator Relation ]
    def equality(self):

        left_tree = self.relation()
        if self.currtok[2] == '==' or self.currtok[2] == '!=':
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            right_tree = self.relation()
            left_tree = ast.BinaryExpr(left_tree, right_tree, tmpID)
        return left_tree

    # Grammar: Relation => Addition [ RelOperator Addition ]
    def relation(self):

        left_tree = self.addition()
        if self.currtok[2] == '<' or self.currtok[2] == '<=' or \
                self.currtok[2] == '>' or self.currtok[2] == '>=':
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            right_tree = self.addition()
            left_tree = ast.BinaryExpr(left_tree, right_tree, tmpID)
        return left_tree

    # Grammar: Addition => Term  { AddOperator Term }
    def addition(self):
        left_tree = self.term()

        while self.currtok[0] == 'PLUS' or self.currtok[0] == "MINUS":
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            right_tree = self.term()
            left_tree = ast.BinaryExpr(left_tree, right_tree, tmpID)

        return left_tree

    # Grammar: Term => Factor {MulOperator Factor}
    def term(self):

        left_tree = self.expon()

        while self.currtok[0] == 'MULTIPLY' or self.currtok[0] == "DIVIDE" or self.currtok[0] == "MOD":
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            right_tree = self.expon()
            left_tree = ast.BinaryExpr(left_tree, right_tree, tmpID)

        return left_tree

    def expon(self):

        left_tree = self.factor()

        while self.currtok[0] == 'EXPONENTIATION':
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            right_tree = self.factor()
            left_tree = ast.BinaryExpr(left_tree, right_tree, tmpID)

        return left_tree

    # Grammar: Factor => [UnaryOperator] Primary
    def factor(self):

        if self.currtok[0] == 'MINUS' or self.currtok[0] == "NOT":
            self.currtok = next(self.tokens)
            tree = self.primary()
            return ast.UnaryExpr(tree)
        else:
            return self.primary()

    # Grammar: Primary => Identifier | IntLit | FloatLit | "(" Expression ")"
    def primary(self):

        if self.currtok[0] == 'IDENTIFIER':
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            return ast.IdExpr(tmpID)
        elif self.currtok[0] == 'INTNUM':
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            return ast.IdExpr(tmpID)
        elif self.currtok[0] == 'REALNUM':
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            return ast.IdExpr(tmpID)
        elif self.currtok[0] == "KWDTRUE":
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            return ast.IdExpr(tmpID)
        elif self.currtok[0] == "KWDFALSE":
            tmpID = self.currtok[2]
            self.currtok = next(self.tokens)
            return ast.IdExpr(tmpID)
        elif self.currtok[0] == 'PCTLPAR':
            self.currtok = next(self.tokens)
            tree = self.expression()
            if self.currtok[0] == 'PCTRPAR':
                self.currtok = next(self.tokens)
                return tree
            else:
                raise CLiteSyntaxError("Right parenthesis expected", self.currtok[1])
        else:
            raise CLiteSyntaxError("Unexpected token:", self.currtok[1])

# Class for errors
class CLiteSyntaxError(Exception):
    def __init__(self, msg, linenum):
        self.msg = msg
        self.linenum = linenum

    def __str__(self):
        return str(self.msg) + self.linenum


if __name__ == '__main__':
    parser = Parser("test.c")

    try:
        tree = parser.parse()
        print(tree)
    except CLiteSyntaxError as e :
        details = str(e.args[0]) + ", " + str(e.args[1])
        print(details)

