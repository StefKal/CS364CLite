"""
Abstract Syntax Representation of Clite programs
"""

indent_level = 0


class Program:
    def __init__(self, decls, stmts):
        # decls is dict
        # stmts is list

        self.decls = decls
        self.stmts = stmts

    def run(self):
        for s in self.stmts:
            s.eval()

    def __repr__(self):
        return "Program({0} {1})".format(repr(self.decls), (repr(self.stmts)))

    def __str__(self):
        return indent_level*'\t' + "int main ( ) {\n" + str(self.decls) + str(self.stmts) + "\n" + indent_level*'\t' + "}"




class decls:

    def __init__(self, aList):
        self.aList = aList

    def __str__(self):

        i = 0
        s = ""
        while i < len(self.aList):

            s += self.aList[i]
            i += 1
        return str(s)


class decl:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    # (needs to be hashable)
    def __eq__(self, other):
        return self.name == other

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "Declaration ({0}, {1})".format(str(self.name), str(self.type))

    def __str__(self):
        return indent_level*'\t' + str(self.type) + " " + str(self.name) + ';' + '\n'


class Stmts:
    def __init__(self, aList):
        self.aList = aList

    def __str__(self):
        i = 0
        s = ""
        while i < len(self.aList):
            s += self.aList[i]
            i += 1
        return str(s)


class SemiStmt:
    def __init__(self):
        pass

    def run(self):
        return


class Block:
    def __init__(self, statement):
        self.statement = statement


    def __str__(self):

        return indent_level * '\t' + "{\n" + str(self.statement) + (indent_level) * '\t' + "}\n"


class assignment:
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def __repr__(self):
        return "{0} = {1}".format(str(self.id), str(self.expr))

    def __str__(self):
        return indent_level*'\t' + str(self.id) + ' = ' + str(self.expr) + ';\n'


class IfStmt:
    def __init__(self, cond, stmt, elsestmt = None):
        self.cond = cond
        self.stmt = stmt
        self.elsestmt = elsestmt

    def __repr__(self):

        return "If({0} {1} {2})".format(str(self.cond), str(self.stmt), str(self.elsestmt))


    def __str__(self):

        if self.elsestmt is None:
            return indent_level*'\t' + "if" + str(self.cond) + "\n\t" + str(self.stmt)
        else:
            return indent_level*'\t' + "if" + str(self.cond) + "\n\t" \
                + str(self.stmt) + indent_level*'\t' + "else" + "\n\t" + str(self.elsestmt) + "\n"


class PrintStmt:
    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return "Print({0})".format(str(self.body))

    def __str__(self):
        return indent_level*'\t' + "print" + "(" + str(self.body) + ")"


class WhileStmt:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def __repr__(self):
        return "While({0} {1})".format(str(self.cond), str(self.body))

    def __str__(self):
        global indent_level
        return indent_level*'\t' + "While" + str(self.cond) + "\n" + str(self.body)

class BinaryExpr:

    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

    def __repr__(self):
        return "BinaryExpr({0} {1})".format(str(self.left), str(self.right))

    def __str__(self):
        return "(" + str(self.left) + " " + str(self.operator) + " " + str(self.right) + ")"

    def run(self):
        if self.operator == '+':
            return eval(self.left) + eval(self.right)
        elif self.operator == '-':
            return eval(self.left) - eval(self.right)
        elif self.operator == '*':
            return eval(self.left) * eval(self.right)
        elif self.operator == '/':
            return eval(self.left) / eval(self.right)
        elif self.operator == '%':
            return eval(self.left) % eval(self.right)


class UnaryExpr:
    def __init__(self, expr, operator):
        self.expr = expr
        self.operator = operator

    def __repr__(self):
        return "UnaryExpr({0})".format(str(self.expr))

    def __str__(self):
        return self.operator + self.expr

    def run(self):
        if self.operator == '-':
            return -(eval(self.expr))
        elif self.operator == '!':
            return not (eval(self.expr))


class IdExpr:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "IdExpr({0})".format(str(self.name))

    def __str__(self):
        return str(self.name)

