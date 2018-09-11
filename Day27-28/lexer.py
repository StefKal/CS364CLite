import os
import re
import sys


def Counter():
    i = 0
    while True:
        yield i
        i += 1


class Lexer:
    """
    The Lexer class analyzes Clite tokens
    """

    # Constants that represent token classifiers
    cnt = Counter()

    # operators
    OR = next(cnt)
    AND = next(cnt)
    EQUAL = next(cnt)
    NOTEQUAL = next(cnt)
    LESS = next(cnt)
    LESSEQ = next(cnt)
    GREATEREQ = next(cnt)
    GREATER = next(cnt)
    PLUS = next(cnt)
    MINUS = next(cnt)
    MULTIPLY = next(cnt)
    DIVIDE = next(cnt)
    MOD = next(cnt)
    NOT = next(cnt)
    ASSIGNMENT = next(cnt)
    EXPONENTIATION = next(cnt)

    # keywords
    KWDPRINT = next(cnt)
    KWDBOOL = next(cnt)
    KWDELSE = next(cnt)
    KWDFALSE = next(cnt)
    KWDIF = next(cnt)
    KWDTRUE = next(cnt)
    KWDFLOAT = next(cnt)
    KWDINT = next(cnt)
    KWDWHILE = next(cnt)
    KWDMAIN = next(cnt)

    # punctuation
    PCTSEMI = next(cnt)
    PCTCOMA = next(cnt)
    PCTLBRA = next(cnt)
    PCTRBRA = next(cnt)
    PCTLPAR = next(cnt)
    PCTRPAR = next(cnt)

    ID = next(cnt)
    REALNUM = next(cnt)
    INTNUM = next(cnt)

    FILENOTFOUND = next(cnt)
    ILLEGALTOKEN = next(cnt)
    EOF = next(cnt)

    # precompile the regex of patterns
    # to split tokens on.
    split_patt = re.compile(

        """
        # O P E R A T O R S 
        \s    |    # whitespace
        (\+)  |    # operator +
        (-)   |    # operator - 
        (<=)  |    # operator <=
        (<)   |    # operator <
        (//)  |
        (\|\|)|    # operator ||
        (&&)  |    # operator &&
        (==)  |    # operator ==
        (!=)  |    # operator !=
        (>=)  |    # operator >=
        (>)   |    # operator >
        (\*\*)|
        (\*)  |    # operator *
        (/)   |    # operator /
        (%)   |    # operator %
        (!)   |    # operator !
        (=)   |    # operator =
        
        # P U N C T U A T I O N S 
        (;) |   # punctuation ;
        (,) |   # punctuation ,
        ({) |   # punctuation {
        (}) |   # punctuation }
        (\()|   # punctuation (
        (\))|   # punctuation )
        (") 
   
        
         """,
        re.VERBOSE
    )

    # regular expression (regex) for an identifier
    id_patt = re.compile("^[a-zA-Z][a-zA-Z0-9_]*$")

    # regex for a real number
    rnum_patt = re.compile("^[0-9]+\.[0-9]*$")
    inum_patt = re.compile("^[0-9]*$")
    str_patt = re.compile("^[\"][\"]$")

    # token dictionary
    td = {
        '||': OR,
        '&&': AND,
        '==': EQUAL,
        '!=': NOTEQUAL,
        '<': LESS,
        '<=': LESSEQ,
        '>=': GREATEREQ,
        '>': GREATER,
        '+': PLUS,
        '-': MINUS,
        '**': EXPONENTIATION,
        '*': MULTIPLY,
        '/': DIVIDE,
        '%': MOD,
        '!': NOT,
        '=': ASSIGNMENT


    }

    # Keyword Dictionary
    kwd = {
        'print': KWDPRINT,
        'bool': KWDBOOL,
        'else': KWDELSE,
        'false': KWDFALSE,
        'if': KWDIF,
        'true': KWDTRUE,
        'float': KWDFLOAT,
        'int': KWDINT,
        'while': KWDWHILE,
        'main' : KWDMAIN
    }

    # Punctuation Dictionary
    pd = {
        ';': PCTSEMI,
        ',': PCTCOMA,
        '{': PCTLBRA,
        '}': PCTRBRA,
        '(': PCTLPAR,
        ')': PCTRPAR,
    }

    # Reverse Dictionary that prints the name of operators/operations
    named = {
        0: 'OR', 1: 'AND', 2: 'EQUAL', 3: 'NOTEQUAL', 4: 'LESS', 5: 'LESSEQ', 6: 'GREATEREQ',
        7: 'GREATER', 8: 'PLUS', 9: 'MINUS', 10: 'MULTIPLY', 11: 'DIVIDE', 12: 'MOD', 13: 'NOT',
        14: 'ASSIGNMENT', 15:'EXPONENTIATION', 16: 'KWDPRINT', 17: 'KWDBOOL', 18: 'KWDELSE', 19: 'KWDFALSE', 20: 'KWDIF',
        21: 'KWDTRUE', 22: 'KWDFLOAT', 23: 'KWDINT', 24: 'KWDWHILE', 25: 'KWDMAIN', 26: 'PCTSEMI',
        27: 'PCTCOMA',28: 'PCTLBRA', 29: 'PCTRBRA', 30: 'PCTLPAR', 31: 'PCTRPAR'
    }


    def token_generator(self, filename):
        # start at 0
        pc = 0
        try:
            file = open(filename)
        except OSError:
            print("Could not read file:", filename)
            sys.exit(1)

        except TypeError:
            print("Invalid number of arguments")
            sys.exit(1)

        for line in file:
            tokens = Lexer.split_patt.split(line)
            tokens = [t for t in tokens if t]
            pc += 1
            # list comp for finding indexes quotes in tokens for stringLit
            indices = [i for i, x in enumerate(tokens) if x == '"']

            for t in tokens:
                # break out of loop if it is a comment
                if t.startswith("//"):
                    break

                if t in Lexer.td:
                    # check if token
                    yield (Lexer.named[Lexer.td[t]], "LineNum: " + str(pc), t)

                # check if punctuation
                elif t in Lexer.pd:
                    yield (Lexer.named[Lexer.pd[t]], "LineNum: " + str(pc), t)

                # check if it matches our identifier pattern
                elif Lexer.id_patt.search(t):
                    if t in Lexer.kwd:
                        # check if keyword first
                        yield (Lexer.named[Lexer.kwd[t]], "LineNum: " + str(pc), t)
                    else:
                        yield ("IDENTIFIER", "LineNum: " + str(pc), t)

                # if it contains quotes -> string literal
                elif indices and indices.__len__() > 1:
                    yield ("STRINGLIT", "LineNum: " + str(pc), tokens[indices[0]:indices[1] + 1])
                    break

                # check if it matches our real number pattern
                elif Lexer.rnum_patt.search(t):
                    yield ("REALNUM", "LineNum: " + str(pc), t)

                # check if it matches our integer patter
                elif Lexer.inum_patt.search(t):
                    yield ("INTNUM", "LineNum: " + str(pc), t)

                # everything else is illegal
                else:
                    yield ("ILLEGALTOKEN", "LineNum: " + str(pc), "Token: " + str(t))

        #indicate end of file
        yield ("END OF FILE line: " + str(pc))


# test main
if __name__ == "__main__":

    script_dir = os.path.dirname(__file__)
    rel_path = "lexertest.c"
    abs_file_path = os.path.join(script_dir, rel_path)
    lex = Lexer()
    tg = lex.token_generator(abs_file_path)

    while True:
        try:
            tok = next(tg)
            print(tok)
        except StopIteration:
            break
